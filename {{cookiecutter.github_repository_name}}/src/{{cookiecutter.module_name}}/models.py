import datetime
import uuid

from decimal import Decimal
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django_rehive_extras.models import DateModel
from django_rehive_extras.fields import MoneyField
from enumfields import EnumField

from {{cookiecutter.module_name}}.enums import CompanyMode, TransactionStatusEnum, WebhookEvent, APISelectionEnum
from {{cookiecutter.module_name}}.utils import from_cents, to_cents


class Company(DateModel):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    admin = models.OneToOneField(
        '{{cookiecutter.module_name}}.User',
        related_name='admin_company',
        on_delete=models.CASCADE
    )
    secret = models.UUIDField()
    active = models.BooleanField(default=True, blank=False, null=False)
    mode = EnumField(CompanyMode, blank=True, null=True)

    def __str__(self):
        return self.identifier

    def natural_key(self):
        return (self.identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.secret = uuid.uuid4()

        return super(Company, self).save(*args, **kwargs)


class User(DateModel):
    identifier = models.UUIDField(unique=True, db_index=True)
    token = models.CharField(max_length=200, null=True)
    company = models.ForeignKey(
        '{{cookiecutter.module_name}}.Company',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.identifier)


class ExternalCurrency(DateModel):
    """
    Model used for storing details of the external ledgers currencies. 

    Can be extended as needed for any unique fields on the external ledger.
    """
    code = models.CharField(max_length=30, db_index=True)
    divisibility = models.IntegerField(default=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_crypto = models.BooleanField(default=False, blank=False, null=False)
    chain = models.CharField(max_length=30, null=True, blank=True)
    destination_prefix = models.CharField(max_length=50, null=True, blank=True)


class Currency(DateModel):
    """
    Model used for storing a companies Rehive currency objects internally. 

    The external_currency field signifies which Rehive currency is linked to which externa ledger currency.
    """
    company = models.ForeignKey(
        '{{cookiecutter.module_name}}.Company',
        null=True,
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=30, db_index=True)
    display_code = models.CharField(max_length=12, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=30, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    divisibility = models.IntegerField(default=2)
    external_currency = models.ForeignKey(
        '{{cookiecutter.module_name}}.ExternalCurrency',
        null=True,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        unique_together = [('company', 'code'), ('company', 'external_currency')]
    
    def __init__(self, *args, **kwargs):
        super(Currency, self).__init__(*args, **kwargs)
        self._original_wyre_code = self.wyre_code

    def __str__(self):
        return str(self.code)

    def set_as_rehive_manager(self):
        rehive = Rehive(self.company.admin.token)
        rehive.admin.currencies.patch(
            self.code,
            manager=str(self.company.admin.identifier)
        )
        # Spin-off a sync task managing currency conversion pairs
        sync_currency_conversion_pairs.delay(rehive_code=self.code, company_id=str(self.company.identifier))


class Transaction(DateModel):
    """
    Model that stores information required to sync a transaction between Rehive and a third party

    This should be extended to include any custom fields required to hande third party transactions
    """
    identifier = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4
    )
    amount = MoneyField(default=Decimal(0), null=True, blank=True)
    company = models.ForeignKey(
        '{{cookiecutter.module_name}}.Company',
        null=True,
        on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        '{{cookiecutter.module_name}}.Currency',
        null=True,
        on_delete=models.CASCADE
    )
    native_id = models.CharField(max_length=200, null=True)
    native_partner_id = models.CharField(max_length=200, null=True)
    native_collection_id = models.CharField(max_length=200, null=True, blank=True)
    native_response = JSONField(null=True, blank=True)
    native_metadata = JSONField(null=True, blank=True)
    third_party_id = models.CharField(max_length=200, null=False)
    third_party_data = JSONField(null=True, blank=True)
    third_party_error = models.TextField(null=True)
    status = EnumField(
        TransactionStatusEnum,
        max_length=32
    )

    def update_model_from_rehive(self):
        """
        Updates the model with the latest Rehive data
        """
        raise Exception('Not implemented')

    def update_model_from_third_party_ledger(self):
        """
        Updates the model with the latest third party data
        """
        raise Exception('Not implemented')

    
    def update_rehive_from_model(self):
        """
        Updates Rehive with the models stored data
        """
        rehive = Rehive(self.company.admin.token)
        # TODO: Add better Rehive error handling
        # TODO: Move this into something that can handle retries
        # Store an error field - connection_error etc
        # Use idompotency for retries
            # Need some manual way to sort out idom errors
        # Create a seperate TransactionTask model which stores the calls the service makes to either Rehive or the third party
            # Last sync'd datefield for both APIs
            # Has sync'd boolean for either API - could store the syncing errors and show if things should be retried or not
        if self.status == TransactionStatusEnum.COMPLETE:
            r = rehive.admin.transaction_collections.confirm(
                self.native_collection_id,
                metadata=self.generate_rehive_metadata()
            )
        elif self.status == TransactionStatusEnum.FAILED:
            # Fail the transaction
            r = rehive.admin.transaction_collections.fail(
                self.native_collection_id,
                metadata=self.generate_rehive_metadata()
            )
            # Append the failure reasons
            self.update_rehive_error_objects()
        self.native_response = r.json()
        self.save()
        return self
            

    def update_third_party_ledger_from_model(self):
        """
        Updates the third party ledger with the models stored data
        """
        # TODO: Remove this and include custom third party calling logic. For now this just assumes a success and keeps moving.
        successfully_completed_on_third_party = True
        if successfully_completed_on_third_party:
            self.status = TransactionStatusEnum.COMPLETE
        else:
            self.status = TransactionStatusEnum.FAILED
        self.save()
        return self
        
    
    def generate_rehive_metadata(self):
        """
        Function that generates a standard metadata structure that is appended to Rehive transactions

        TODO: Standardise third party ledger display information metadata space
        """
        metadata = {
            '{{cookiecutter.module_name}}_context': {
                'id': str(self.third_party_id)
            },
            'native_context': {
                'transaction_display_details': {
                    'hash': self.third_party_data.get('hash')
                }
            }
        }
        return metadata


    def update_rehive_error_objects(self):
        rehive = Rehive(self.company.admin.token)
        if self.native_id:
            rehive.admin.transactions.obj(self.native_id).messages.create(
                level='error',
                section='user',
                message=self.third_party_error
            )
        if self.native_partner_id:
            rehive.admin.transactions.obj(self.native_partner_id).messages.create(
                level='error',
                section='user',
                message=self.third_party_error
            )


    @classmethod
    def create_from_rehive_transfer(cls, tx_data, company):
        # TODO: Combine these two functions
        currency = Currency.objects.get(
            code=tx_data.get('currency').get('code'),
            company=company
        )
        transaction = cls.objects.create(
            amount=from_cents(
                abs(tx_data.get('amount')),
                currency.divisibility
            ),
            native_metadata=tx_data.get('metadata'),
            native_id=tx_data.get('id'),
            native_collection_id=tx_data.get('collection_id'),
            native_partner_id=tx_data.get('partner').get('id'),
            status=TransactionStatusEnum.PENDING,
            company=company
        )
        transaction.update_third_party_ledger_from_model()
        transaction.update_rehive_from_model()
    
    @classmethod
    def create_from_rehive_debit(cls, tx_data, company):
        currency = Currency.objects.get(
            code=tx_data.get('currency').get('code'),
            company=company
        )
        transaction = cls.objects.create(
            amount=from_cents(
                abs(tx_data.get('amount')),
                currency.divisibility
            ),
            native_metadata=tx_data.get('metadata'),
            native_id=tx_data.get('id'),
            native_collection_id=tx_data.get('collection_id'),
            status=TransactionStatusEnum.PENDING,
            company=company
        )
        transaction.update_third_party_ledger_from_model()
        transaction.update_rehive_from_model()


class TransactionSyncTask(DateModel):
    """
    Model which stores the attempts and responses made to update a third party with internal transaction data
    """
    identifier = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4
    )
    transaction = models.ForeignKey(
        '{{cookiecutter.module_name}}.Transaction',
        null=True,
        on_delete=models.CASCADE
    )
    transaction_snapshot = JSONField(null=True, blank=True)
    api = EnumField(APISelectionEnum, max_length=100, null=True, blank=True)
    api_response = JSONField(null=True, blank=True)
    completed = models.DateTimeField(null=True)
    failed = models.DateTimeField(null=True)
    tries = models.IntegerField(default=0)

    # Max number of retries allowed.
    MAX_RETRIES = 6

    def process(self):
        # Sync transaction with Rehive
        if self.api == APISelectionEnum.NATIVE:
            
        # Sync transaction with third party
        elif self.api == APISelectionEnum.THIRD_PARTY:



class PlatformWebhook(DateModel):
    """
    Model used to store all Rehive webhooks sent to the service.

    Includes both the data and if it was successfully processed or not.
    """
    identifier = models.CharField(max_length=64, unique=True)
    company = models.ForeignKey(
        '{{cookiecutter.module_name}}.Company', on_delete=models.CASCADE
    )
    event = EnumField(WebhookEvent, max_length=100, null=True, blank=True)
    data = JSONField(null=True, blank=True)
    # State data.
    completed = models.DateTimeField(null=True)
    failed = models.DateTimeField(null=True)
    tries = models.IntegerField(default=0)

    # Max number of retries allowed.
    MAX_RETRIES = 6

    class Meta:
        unique_together = ('identifier', 'company',)

    def __str__(self):
        return str(self.identifier)

    def process_async(self):
        from {{cookiecutter.module_name}}.tasks import process_platform_webhook
        logger.info('Delaying a task for processing Rehive webhook')
        try:
            process_platform_webhook.delay(self.id)
        except Exception as exc:
            logger.info(exc)
            raise exc

    def process(self):
        # Increment the number of tries.
        self.tries = self.tries + 1

        try:
            if self.event in (WebhookEvent.CURRENCY_CREATE,
                              WebhookEvent.CURRENCY_UPDATE,):
                # Update or create the currency.
                currency, created = Currency.objects.update_or_create(
                    code=self.data["code"],
                    company=self.company,
                    defaults={
                        "display_code": self.data['display_code'],
                        "description": self.data['description'],
                        "symbol": self.data['symbol'],
                        "unit": self.data['unit'],
                        "divisibility": self.data['divisibility']
                    }
                )
            if self.event == WebhookEvent.TRANSACTION_INITIATE:
                logger.info('Processing initiated transaction webhook')
                process_transaction_initiated_webhook.delay(
                    tx_data=self.data,
                    company=str(self.company.identifier)
                )
            if self.event == WebhookEvent.ACCOUNT_CREATE:
                logger.info('Processing account created webhook')
                process_account_created.delay(
                    data=self.data,
                    company=str(self.company.identifier)
                )
        except Exception as exc:
            self.failed = now() if self.tries > self.MAX_RETRIES else None
            self.save()
            logger.exception(exc)
            raise PlatformWebhookProcessingError(exc)
        else:
            self.completed = now()
            self.save()
