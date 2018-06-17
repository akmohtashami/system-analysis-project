"""proxypay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.contrib.staticfiles.views import static
from django.contrib import admin
from django.urls import path, re_path, include

from proxypay.views import IndexView

urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('', include('users.urls', namespace='users')),
    re_path('', include('wallet.urls', namespace='wallets')),
    re_path('^services/', include('services.urls', namespace='services')),
    re_path('', include('static_pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),

    path('contact/', static.serve, kwargs={
            'path': 'contact.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('send-email/', static.serve, kwargs={
            'path': 'send-email.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('change_password/', static.serve, kwargs={
            'path': 'change-password.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('wallet/', static.serve, kwargs={
            'path': 'wallet.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('exchange/', static.serve, kwargs={
            'path': 'exchange.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('exchange/confirm', static.serve, kwargs={
            'path': 'exchange-confirm.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('exchange_rate/', static.serve, kwargs={
            'path': 'exchange-rate.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('change_exchange_fee/', static.serve, kwargs={
            'path': 'change-exchange-fee.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('simulate_exchange/', static.serve, kwargs={
            'path': 'simulate-exchange.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('charge/', static.serve, kwargs={
            'path': 'rial-charge-request.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('charge/confirm/', static.serve, kwargs={
            'path': 'rial-charge-confirm.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('handle_request/', static.serve, kwargs={
        'path': 'requests-list.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('handle_request/1/', static.serve, kwargs={
        'path': 'request-detail.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('requests/', static.serve, kwargs={
        'path': 'request-types-list.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('requests/add/', static.serve, kwargs={
        'path': 'request-type-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('requests/toefl/edit/', static.serve, kwargs={
        'path': 'request-type-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/toefl/', static.serve, kwargs={
        'path': 'request-type-description.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/toefl/confirm/', static.serve, kwargs={
        'path': 'request-type-confirm.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('requests/history/', static.serve, kwargs={
        'path': 'request-history.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('pages/', static.serve, kwargs={
        'path': 'static-pages-list.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('pages/add/', static.serve, kwargs={
        'path': 'static-page-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('pages/static_page/edit/', static.serve, kwargs={
        'path': 'static-page-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('page/static_page/', static.serve, kwargs={
        'path': 'static-page-description.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),

    path('withdraw/', static.serve, kwargs={
        'path': 'withdraw-request.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
]
