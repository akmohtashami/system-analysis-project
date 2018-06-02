from enumfields import Enum, EnumField

from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wallet.models import Currency


class RequestTypeStatus(Enum):
    show = 'Show'
    hide = 'Hide'


class RequestType(models.Model):
    short_name = models.CharField(
        verbose_name=_("short name"),
        unique=True,
        null=False,
        validators=[URLValidator()]
    )
    name = models.CharField(
        verbose_name=_("name")
    )
    currency = EnumField(
        Currency,
        verbose_name=_("currency")
    )
    fee = models.IntegerField(
        verbose_name=_("transaction fee"),
        default=0
    )
    status = EnumField(
        RequestTypeStatus,
        verbose_name=_("status")
    )
