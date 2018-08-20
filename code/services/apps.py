from django.apps import AppConfig
from django.db.models.signals import class_prepared
from django.utils.translation import ugettext as _


class ServicesConfig(AppConfig):
    name = 'services'

