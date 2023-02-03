import uuid

from drf_rehive_extras.fields import EnumField
from rehive import Rehive, APIException
from rest_framework import serializers
from django.db import transaction
from drf_rehive_extras.serializers import BaseModelSerializer

from {{cookiecutter.module_name}}.models import (
    Company, User, Transaction, ExternalCurrency,
    Currency
)
from {{cookiecutter.module_name}}.enums import CompanyMode, TransactionStatusEnum


class ActivateSerializer(serializers.Serializer):
    """
    Serialize the activation data, should be a token that represents an admin
    user.
    """

    token = serializers.CharField(write_only=True)
    id = serializers.CharField(source='identifier', read_only=True)
    name = serializers.CharField(read_only=True)
    secret = serializers.UUIDField(read_only=True)

    def validate(self, validated_data):
        token = validated_data.get('token')
        rehive = Rehive(token)

        try:
            user = rehive.auth.get()
            groups = [g['name'] for g in user['groups']]
            if len(set(["admin", "service"]).intersection(groups)) <= 0:
                raise serializers.ValidationError(
                    {"token": ["Invalid admin user."]})
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid user."]})

        try:
            company = rehive.admin.company.get()
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid company."]})

        validated_data['user'] = user
        validated_data['company'] = company

        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        token = validated_data.get('token')
        rehive_user = validated_data.get('user')
        rehive_company = validated_data.get('company')

        # Activate an existing company.
        try:
            company = Company.objects.get(
                identifier=rehive_company.get('id')
            )
        # If no company exists create a new new admin user and company.
        except Company.DoesNotExist:
            user = User.objects.create(
                token=token,
                identifier=uuid.UUID(rehive_user['id'])
            )
            company = Company.objects.create(
                admin=user,
                identifier=rehive_company.get('id'),
                mode=rehive_company.get('mode')
            )
            user.company = company
            user.save()
        # If company existed then reactivate it.
        else:
            # If reactivating a company using a different service admin then
            # create a new user and set it as the admin.
            if str(company.admin.identifier) != rehive_user["id"]:
                user = User.objects.create(
                    token=token,
                    identifier=uuid.UUID(rehive_user['id']),
                    company=company
                )
                # Remove the token from the old admin.
                old_admin = company.admin
                old_admin.token = None
                old_admin.save()
                # Set the new admin.
                company.admin = user
                company.active = True
                company.save()
            # Else just update the admin token with the new one.
            else:
                company.admin.token = token
                company.admin.save()
                company.active = True
                company.save()

        # Add required currencies to service automatically.
        if currencies:
            for kwargs in currencies:
                currency = Currency.objects.get_or_create(
                    code=kwargs['code'],
                    company=company,
                    defaults={
                        "display_code": kwargs['display_code'],
                        "description": kwargs['description'],
                        "symbol": kwargs['symbol'],
                        "unit": kwargs['unit'],
                        "divisibility": kwargs['divisibility']
                    }
                )

        # Setup webhooks
        service_url = os.environ.get('BASE_DOMAIN')

        # Additional webhooks can be added as needed
        webhooks = (
            {
                "url": '/api/webhook/',
                'event': WebhookEvent.TRANSACTION_EXECUTE.value,
            },
            {
                "url": '/api/webhook/',
                'event': WebhookEvent.TRANSACTION_INITIATE.value,
            },
            {
                "url": '/api/webhook/',
                "event": WebhookEvent.CURRENCY_CREATE.value,
            },
            {
                "url": '/api/webhook/',
                "event": WebhookEvent.CURRENCY_UPDATE.value,
            }
        )

        for webhook in webhooks:
            try:
                rehive.admin.webhooks.create(
                    url=urljoin(service_url, webhook.get('url')),
                    event=webhook.get('event'),
                    secret=str(company.secret),
                )
            except APIException as e:
                if e.status_code == 400:
                    if 'A webhook with the url and event already exists.' == str(e):
                        logger.info('Webhook exists. Skipping.')
                        continue 
                logger.error('Error creating webhook')
                logger.error(e)
                raise serializers.ValidationError(
                    'Error creating Rehive webhooks'
                )

        # If the service uses custom subtypes they can be included in this array to be added on activation
        required_subtypes = []
        try:
            for rs in required_subtypes:
                if (rs['name'] not in [s['name'] for s in subtypes
                        if s['tx_type'] == rs['tx_type']]):
                    rehive.admin.subtypes.create(
                        name=rs['name'],
                        label=rs.get("label"),
                        description=rs.get("description"),
                        tx_type=rs['tx_type']
                    )
        except RehiveAPIException:
            raise serializers.ValidationError(
                {"non_field_errors": ["Unable to configure subtypes."]})

        return company


class DeactivateSerializer(serializers.Serializer):
    """
    Serialize the deactivation data, should be a token that represents an admin
    user.
    """
    token = serializers.CharField(write_only=True)
    purge = serializers.BooleanField(write_only=True, required=False, default=False)

    def validate(self, validated_data):
        token = validated_data.get('token')
        rehive = Rehive(token)

        try:
            user = rehive.auth.get()
            groups = [g['name'] for g in user['groups']]
            if len(set(["admin", "service"]).intersection(groups)) <= 0:
                raise serializers.ValidationError(
                    {"token": ["Invalid admin user."]})
        except APIException:
            raise serializers.ValidationError({"token": ["Invalid user."]})

        try:
            validated_data['company'] = Company.objects.get(
                identifier=user['company'])
        except Company.DoesNotExist:
            raise serializers.ValidationError(
                {"token": ["Company has not been activated yet."]})

        return validated_data

    def delete(self):
        company = self.validated_data['company']
        purge = self.validated_data.get('purge', False)
        if purge is True:
            company.delete()
            return
        company.active = False
        company.admin.token = None
        company.save()
        company.admin.save()


class AdminCompanySerializer(BaseModelSerializer):
    id = serializers.CharField(source='identifier', read_only=True)
    secret = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    mode = EnumField(enum=CompanyMode, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'secret', 'name', 'mode')


class ExternalCurrencySerializer(BaseModelSerializer):

    class Meta:
        model = ExternalCurrency
        fields = (
            'code',
            'divisibility',
            'description',
            'is_crypto',
            'chain',
            'base_chain_code'
        )


class CurrencySerializer(BaseModelSerializer):
    
    class Meta:
        model = Currency
        fields = (
            'company',
            'code',
            'display_code',
            'symbol',
            'unit',
            'divisibility',
            'is_crypto',
            'external_currency'
        )


class AdminCurrencySerializer(CurrencySerializer):
    
    class Meta:
        model = Currency
        fields = (
            'company',
            'code',
            'display_code',
            'symbol',
            'unit',
            'divisibility',
            'is_crypto',
            'external_currency',
        )
        read_only_fields = (
            'company',
            'code',
            'display_code',
            'symbol',
            'unit',
            'divisibility',
            'is_crypto',
        )
    
    def update(self, instance, validated_data):
        if validated_data.get('external_currency'):
            try:
                external_currency = ExternalCurrency.objects.get(
                    code=validated_data.get('external_currency')
                )
                if external_currency.divisibility != instance.divisibility:
                    raise serializers.ValidationError(
                        {"error": ["The external currency and native currency divisibility need to match."]}
                    ) 
                validated_data['external_currency'] = external_currency
            except ExternalCurrency.DoesNotExist as exc:
                raise serializers.ValidationError(
                    {"error": ["External currency code not supported."]}
                )
        return super().update(instance, validated_data)


class TransactionSerializer(BaseModelSerializer):

    status = EnumField(TransferStatusEnum, read_only=True, required=False)
    
    class Meta:
        model = Currency
        fields = (
            'identifier',
            'amount',
            'company',
            'currency',
            'native_id',
            'native_partner_id',
            'native_collection_id',
            'third_party_id',
            'status'
        )
