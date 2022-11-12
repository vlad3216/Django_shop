from os import path
from decimal import Decimal

from django.db import models
from django.core.cache import cache
from django.contrib.auth import get_user_model

from shop1.const import MAX_DIGITS, DECIMAL_PLACES
from shop1.mixins.mod_mix import PKMixin
from shop1.model_choice import Currency
from currencies.models import CurrencyHistory


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/'\
        f'{instance.pk}/image{extension}'


class Category(PKMixin):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to=upload_image
    )

    def __str__(self) -> str:
        return self.name


class Product(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
        )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    products = models.ManyToManyField(
        'products.Product',
        blank=True
    )
    favorites = models.ManyToManyField(
        get_user_model(),
        related_name='favorites',
        blank=True
    )

    @property
    def get_price(self):
        if self.currency != Currency.UAH:
            kurs = CurrencyHistory.objects.filter(
                currency=self.currency
                ).order_by('-created_at').first()
            return Decimal(self.price * kurs.sale).quantize(Decimal('1.00'))
        return self.price

    def __str__(self) -> str:
        return f'{self.name} | {self.price} | {self.sku}'

    @classmethod
    def _cache_key(cls):
        return 'products'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._cache_key())
        if not products:
            products = Product.objects.all()
            cache.set(cls._cache_key(), products)
        return products