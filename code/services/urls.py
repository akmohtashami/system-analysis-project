from django.urls import re_path

from services.views import *

app_name = 'urls'
urlpatterns = [
    re_path(r'^type/add/$', AddServiceTypeView.as_view(), name="add_service_type"),
]
