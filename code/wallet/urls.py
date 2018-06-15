from django.urls import re_path

from wallet.views import *

app_name = 'wallet'
urlpatterns = [
    re_path('^wallets/$', MyWalletsView.as_view(), name='wallets')
]
