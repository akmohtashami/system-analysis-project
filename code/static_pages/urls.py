from django.urls import re_path

from static_pages.views import *

app_name = 'pages'
urlpatterns = [
    re_path(r'^contact/$', SendEmailToManagersView.as_view(), name="send_email_to_managers"),
]
