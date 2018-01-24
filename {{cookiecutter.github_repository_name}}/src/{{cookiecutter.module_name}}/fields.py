from django.db import models


class MoneyField(models.DecimalField):
    """
    Decimal Field with hardcoded precision of 28 and a scale of 18.

    Usage:
    from decimal import Decimal
    field_name = MoneyField(default=Decimal(0))
    """

    def __init__(self, verbose_name=None, name=None, max_digits=28,
                 decimal_places=18, **kwargs):
        super(MoneyField, self).__init__(verbose_name, name, max_digits,
            decimal_places, **kwargs)