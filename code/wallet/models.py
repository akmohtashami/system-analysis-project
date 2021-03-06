from enum import Enum

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from proxypay.fields import EnumField
from users.models import User, UserType


class Currency(Enum):
    IRR = (_('Rial'), 'irr')
    USD = (_('Dollar'), 'usd')
    EUR = (_('Euro'), 'eur')

    def __init__(self, title, icon):
        self.title = title
        self.icon = icon

    def __str__(self):
        return str(self.title)


class Wallet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        related_name="wallets"
    )
    currency = EnumField(
        Currency,
        verbose_name=_("currency")
    )
    credit = models.FloatField(verbose_name=_("credit"), default=0)

    class Meta:
        unique_together = (('currency', 'owner'), )

    @classmethod
    def get_company_wallets(cls):
        user, created = User.objects.get_or_create(id=0, defaults={
            "email": "company@localhost",
            "type": UserType.System,
            "is_active": False
        })
        if created:
            user.set_unusable_password()
            user.save()
            # for currency in Currency:
            #    cls.objects.get_or_create(owner=user, currency=currency)
        return user.wallets.all()


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_wallets_for_new_users")
def create_wallets(sender, instance, created, *args, **kwargs):
    if created:
        for currency in Currency:
            if instance.is_customer() or \
                            instance.type == UserType.System or \
                            currency == Currency.IRR:
                Wallet.objects.create(
                    owner=instance,
                    currency=currency,
                    credit=0
                )