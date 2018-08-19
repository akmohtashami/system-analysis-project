from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from solo.models import SingletonModel


class Config(SingletonModel):
    index_content = models.TextField(verbose_name=_("index content"), default="", blank=True)
    exchange_fee = models.PositiveIntegerField(
        verbose_name=_("exchange fee"),
        default=0
    )