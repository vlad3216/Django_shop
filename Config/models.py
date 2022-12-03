from django.db import models
from shop1.mixins.mod_mix import SingletonModel


class Config(SingletonModel):
    contact_form_email = models.EmailField()