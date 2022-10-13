from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model

from shop1.const import MAX_DIGITS, DECIMAL_PLACES
from shop1.mixins.mod_mix import PKMixin
from shop1.model_choice import DiscountTypes


class Discount(PKMixin):
    amount = models.PositiveSmallIntegerField(
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
        )
    discount_type = models.PositiveIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self) -> str:
        return f'{self.amount} | {self.code}'


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product = models.ManyToManyField("items.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.user} | {self.total_amount}'

    def get_total_amount(self):
        if self.discount:
            if self.discount.discount_type == DiscountTypes.VALUE:
                return self.total_amount - Decimal(
                    self.discount.amount).quantize(Decimal('1.00'))
            else:
                return self.total_amount - Decimal(
                        self.total_amount / 100 * self.discount.amount
                        ).quantize(Decimal('1.00'))
        return self.total_amount