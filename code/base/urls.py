from django.urls import re_path

from base.views import *

urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^edit_index/$', EditIndexView.as_view(), name='edit_index'),
]