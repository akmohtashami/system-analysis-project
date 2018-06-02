from django.urls import re_path

from users.views import *

app_name = 'urls'
urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    #re_path(r'^login/$', RunResult.as_view(), name="run_result"),
]