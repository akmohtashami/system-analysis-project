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
    Admin = 2
    System = 3


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

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
        return self.type == UserType.Admin or self.is_superuser

    def is_employee(self):
        return self.type == UserType.Employee

    def is_customer(self):
        return self.type == UserType.Customer

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def notify_charge(self, amount):
        pass

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

