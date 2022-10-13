from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

from shop.mixins.mod_mix import PKMixin


class Feedback(PKMixin):
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(5),)
    )

    def __str__(self) -> str:
        return f'{self.user} {self.created_at}'