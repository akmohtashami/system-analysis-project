from django.urls import re_path

from services.models import ServiceType
from services.views import *

app_name = 'services'
urlpatterns = [
    re_path(r'^type/add/$', AddServiceTypeView.as_view(), name="add_new_type"),
    re_path(r'^history/$', RequestsHistoryView.as_view(), name="requests_history"),
    re_path(r'^(?P<service_name>{})/$'.format(ServiceType.SHORT_NAME_REGEX),
            ServiceTypeDescriptionView.as_view(), name="service_description"),
]
