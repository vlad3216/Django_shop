from django.db import models

from shop1.const import MAX_DIGITS, DECIMAL_PLACES
from shop1.mixins.mod_mix import PKMixin
from shop1.model_choice import Currency


class CurrencyHistory(PKMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    def __str__(self) -> str:
        return f'{self.currency} | {self.created_at}'