from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.cache import cache

from shop1.mixins.mod_mix import PKMixin


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

    @classmethod
    def _cache_key(cls):
        return 'feedbacks'

    @classmethod
    def get_feedbacks(cls):
        feedbacks = cache.get(cls._cache_key())
        print('BEFORE ', feedbacks)
        if not feedbacks:
            feedbacks = Feedback.objects.all()
            cache.set(cls._cache_key(), feedbacks)
            print('AFTER ', feedbacks)
        return