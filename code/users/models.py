from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from proxypay.fields import EnumField


class UserType(Enum):
    Customer = 0
    Employee = 1
    Admin = 1


class User(AbstractBaseUser, PermissionsMixin):

    objects = BaseUserManager()

    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    monthly_salary = models.PositiveIntegerField(
        verbose_name=_("monthly salary"),
        default=0
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    type = EnumField(UserType, verbose_name=_("type"), default=UserType.Customer)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_admin(self):
        return self.type == UserType.Admin

    def is_employee(self):
        return self.type == UserType.Employee

    def is_customer(self):
        return self.type == UserType.Customer

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

