from django.core.validators import URLValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from proxypay.fields import EnumField
from wallet.models import Currency


class ServiceType(models.Model):
    short_name = models.CharField(
        verbose_name=_("short name"),
        unique=True,
        max_length=255,
        validators=[RegexValidator("^[a-zA-Z0-9\_\-]+$")]
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    currency = EnumField(
        Currency,
        verbose_name=_("currency")
    )
    fee = models.PositiveIntegerField(
        verbose_name=_("transaction fee"),
        default=0
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_("Designate whether this type of requests can be created.")
    )
