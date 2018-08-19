from django.urls import re_path

from wallet.views import *

app_name = 'wallet'
urlpatterns = [
    re_path('^wallets/$', MyWalletsView.as_view(), name='wallets'),
    re_path('^charge/$', UserRialChargeView.as_view(), name='charge'),
    re_path('^exchange/$', UserExchangeView.as_view(), name='exchange'),
    re_path('^company/wallets/$', CompanyWalletsView.as_view(), name='company_wallets'),
    re_path('^company/exchange/$', CompanyExchangeView.as_view(), name='company_exchange'),
    re_path('^rates/$', ExchangeRateView.as_view(), name='rates'),
    re_path('^rates/$', ExchangeRateView.as_view(), name='simulate_exchange'),
]
