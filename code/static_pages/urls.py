from django.urls import re_path

from static_pages.models import StaticPage
from static_pages.views import *

app_name = 'pages'
urlpatterns = [
    re_path(r'^contact/$', SendEmailToManagersView.as_view(), name="send_email_to_managers"),
    re_path(r'^pages/list/$', PagesListView.as_view(), name="pages_list"),
    re_path(r'^pages/add/$', AddPageView.as_view(), name="add_new_page"),
    re_path(r'^pages/(?P<page_name>{})/$'.format(StaticPage.SHORT_NAME_REGEX),
            EditPageView.as_view(), name="edit_page"),
    re_path(r'^(?P<page_name>{})/$'.format(StaticPage.SHORT_NAME_REGEX),
            PageDescriptionView.as_view(), name="page_description"),
]
