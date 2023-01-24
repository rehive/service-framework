


@shared_task(acks_late=True, bind=True, default_retry_delay=60)
def process_platform_webhook(self, webhook_id):
    """
    Task for processing webhooks.
    """

    from {{cookiecutter.module_name}}.models import PlatformWebhook
    from {{cookiecutter.module_name}}.exceptions import PlatformWebhookProcessingError

    logger.info('Processing Rehive webhook task')

    try:
        webhook = PlatformWebhook.objects.get(id=webhook_id)
    except PlatformWebhook.DoesNotExist:
        logger.error('Platform webhook does not exist.')
        return

    try:
        webhook.process()
    except Exception as exc:
        try:
            self.retry(
                max_retries=PlatformWebhook.MAX_RETRIES,
                exc=PlatformWebhookProcessingError
            )
        except PlatformWebhookProcessingError:
            logger.info("Platform webhook exceeded max retries.")


@shared_task
def process_transaction_initiated_webhook(tx_data, company):
    """
    This tasks is triggered whenever a Rehive transaction webhook is recieved

    By default it approves any transaction. This should be updated to handle syncing logic specific to the third party ledger.
    """
    from rehive import Rehive
    from {{cookiecutter.module_name}}.models import Company, Transaction, Currency
    from {{cookiecutter.module_name}}.utils import from_cents
    company = Company.objects.get(identifier=company)

    try:
        # Check if the currency is relevant. Skip otherwise.
        try:
            currency = Currency.objects.get(
                code=tx_data.get('currency').get('code'),
                company=company,
                external_currency__isnull=False
            )
        except Currency.DoesNotExist:
            return

        if tx_data.get('partner'):
            transfer = Transfer.create_from_rehive_transfer(tx_data, company)
        elif tx_data.get('tx_type') == 'debit':
            # Native context withdrawal logic
            transfer = Transfer.create_from_rehive_debit(tx_data, company)
        elif (tx_data.get('tx_type') == 'credit':
            # First check if this is actually a transfer created by the service
            try:
                # Get by the metadata third party id to prevent race conditions
                if (tx_data.get('metadata') and tx_data.get('metadata').get('{{cookiecutter.module_name}}') and tx_data.get('metadata').get('{{cookiecutter.module_name}}').get('id')):
                    Transfer.objects.get(
                        third_party_id=tx_data.get('metadata').get('{{cookiecutter.module_name}}').get('id'),
                        native_id=tx_data.get('id')
                    )
                else:
                    # Manual credits should be failed
                    # TODO: Add error message to transaction errors list
                    rehive = Rehive(company.admin.token)
                    rehive_tx = rehive.admin.transactions.fail(
                        tx_data.get('id'),
                        metadata={
                            '{{cookiecutter.module_name}}': {'error': 'Manual credits cannot be processed.'}
                        }
                    )
                    return
            except Transfer.DoesNotExist:
                # Manual credits should be failed
                # TODO: Add error message to transaction errors list
                rehive = Rehive(company.admin.token)
                rehive_tx = rehive.admin.transactions.fail(
                    tx_data.get('id'),
                    metadata={
                        '{{cookiecutter.module_name}}': {'error': 'Manual credits cannot be processed.'}
                    }
                )
                return
    except Exception as exc:
        # TODO: Add better error handling logic
        rehive = Rehive(company.admin.token)
        rehive_tx = rehive.admin.transactions.fail(
            tx_data.get('id'),
            metadata={
                '{{cookiecutter.module_name}}': {'error': 'Service could not process the transaction.'}
            }
        )
        raise exc