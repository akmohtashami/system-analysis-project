from enum import Enum

import markdown
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator, MinValueValidator
from django.db import models
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from proxypay.fields import EnumField
from wallet.models import Currency


class ServiceType(models.Model):
    SHORT_NAME_REGEX = "[a-zA-Z0-9\_\-]+"
    short_name = models.CharField(
        verbose_name=_("short name"),
        unique=True,
        max_length=255,
        validators=[RegexValidator('^{}$'.format(SHORT_NAME_REGEX))]
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
    description = models.TextField(
        verbose_name=_("description"),
        blank=True
    )

    def user_can_make_request(self, user):
        return (user.is_authenticated and
                (user.is_customer() or self.short_name == 'withdraw'))

    def clean(self):
        super(ServiceType, self).clean()
        if self.short_name == 'withdraw' and self.currency != Currency.IRR:
            raise ValidationError(_("Withdraw is only allowed from IRR account"))

    @property
    def description_html(self):
        return markdown.markdown(self.description)

    def __str__(self):
        return self.name


class RequestStatus(Enum):
    PENDING = _("Pending"),
    DONE = _("Done")
    REJECTED = _("Rejected")

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return str(self.title)


class ServiceRequest(models.Model):
    service_type = models.ForeignKey(ServiceType, verbose_name=_("service type"), on_delete=models.PROTECT,
                                     related_name='requests')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("owner"), on_delete=models.PROTECT,
                              related_name='requests')
    amount = models.FloatField(verbose_name=_("amount"), validators=[MinValueValidator(0)])
    currency = EnumField(
        Currency,
        verbose_name=_("currency")
    )
    description = models.TextField(verbose_name=_("description"), blank=True)
    status = EnumField(RequestStatus, verbose_name=_("status"), default=RequestStatus.PENDING)
    creation_date = models.DateField(auto_now_add=True, verbose_name=_("creation date"))


@receiver(class_prepared, sender=ServiceType)
def create_withdraw_request(sender, **kwargs):
    sender.objects.get_or_create(
        short_name='withdraw',
        defaults={
            "name": _("Withdraw"),
            "currency": Currency.IRR
        }
    )