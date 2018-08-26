from django.urls import re_path, path

from services.models import ServiceType
from services.views import *

app_name = 'services'
urlpatterns = [
    re_path(r'^type/add/$', AddServiceTypeView.as_view(), name="add_new_type"),
    re_path(r'^history/$', RequestsHistoryView.as_view(), name="requests_history"),
    re_path(r'^withdraw/$'.format(ServiceType.SHORT_NAME_REGEX),
            WithdrawRequestView.as_view(), name="withdraw"),
    re_path(r'^list/$', RequestsListView.as_view(), name="requests_list"),
    re_path(r'^type/list/$', ServiceTypeListView.as_view(), name="service_type_list"),
    path('<uuid:link>/', RequestDetailsView.as_view(), name="details"),
    re_path(r'^type/(?P<service_name>{})/$'.format(ServiceType.SHORT_NAME_REGEX),
            ServiceTypeDetailsView.as_view(), name="service_type_details"),
    re_path(r'^(?P<service_name>{})/$'.format(ServiceType.SHORT_NAME_REGEX),
            ServiceTypeDescriptionView.as_view(), name="service_description"),
]
