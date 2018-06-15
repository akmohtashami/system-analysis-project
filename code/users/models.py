from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


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
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = (('admin_access', _("Admin")),
                       ('employee_access', _("Employee")),
                       ('customer_access', _("Customer")))

    def is_admin(self):
        return self.has_perm('admin_access')

    def is_employee(self):
        return self.has_perm('employee_access')

    def is_customer(self):
        return self.has_perm('customer_access')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

