from django.urls import re_path

from users.views import *

app_name = 'users'
urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^login/$', LoginView.as_view(), name="login"),
    re_path(r'^logout/$', LogoutView.as_view(), name="logout"),
]