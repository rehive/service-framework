from enum import Enum


class CompanyMode(Enum):
    TEST = 'test'
    PRODUCTION = 'production'

    class Labels:
        TEST = 'test'
        PRODUCTION = 'production'


class WebhookEvent(Enum):
    CURRENCY_CREATE = 'currency.create'
    CURRENCY_UPDATE = 'currency.update'
    TRANSACTION_INITIATE = 'transaction.initiate'
    TRANSACTION_EXECUTE = 'transaction.execute'
    ACCOUNT_CREATE = 'account.create'
    USER_UPDATE = 'user.update'

    class Labels:
        CURRENCY_CREATE = 'currency.create'
        CURRENCY_UPDATE = 'currency.update'
        TRANSACTION_INITIATE = 'transaction.initiate'
        TRANSACTION_EXECUTE = 'transaction.execute'
        ACCOUNT_CREATE = 'account.create'
        USER_UPDATE = 'user.update'


class TransactionStatusEnum(Enum):
    INITIATED = 'INITIATED'
    PENDING = 'PENDING'
    COMPLETE = 'COMPLETE'
    FAILED = 'FAILED'

    class Labels:
        INITIATED = 'INITIATED'
        PENDING = 'PENDING'
        COMPLETE = 'COMPLETE'
        FAILED = 'FAILED'


class APISelectionEnum(Enum):
    REHIVE = 'REHIVE'
    THIRD_PARTY = 'THIRD_PARTY'

    class Labels:
        REHIVE = 'REHIVE'
        THIRD_PARTY = 'THIRD_PARTY'