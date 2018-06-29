from django.urls import re_path

from users.views import *

app_name = 'users'
urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^register_with_link/$', RegisterWithLinkView.as_view(), name="register_with_link"),
    re_path(r'^login/$', LoginView.as_view(), name="login"),
    re_path(r'^logout/$', LogoutView.as_view(), name="logout"),
    re_path(r'^change_password/$', ChangePasswordView.as_view(), name="change_password"),
    re_path(r'^inform/$', SendEmailToUsersView.as_view(), name="send_email_to_users"),
]
