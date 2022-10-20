from os import path

from django.db import models

from shop1.const import MAX_DIGITS, DECIMAL_PLACES
from shop1.mixins.mod_mix import PKMixin


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
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    products = models.ManyToManyField('products.Product', blank=True)

    def __str__(self) -> str:
        return f'{self.name} | {self.price} | {self.sku}'