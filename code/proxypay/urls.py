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
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', static.serve, kwargs={
            'path': 'contact.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('register/', static.serve, kwargs={
            'path': 'register.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('charge/', static.serve, kwargs={
            'path': 'rial-charge-request.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('charge/confirm/', static.serve, kwargs={
            'path': 'rial-charge-confirm.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('charge/done/', static.serve, kwargs={
        'path': 'rial-charge-done.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('handle_request/', static.serve, kwargs={
        'path': 'requests-list.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('handle_request/1/', static.serve, kwargs={
        'path': 'request-detail.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('requests/', static.serve, kwargs={
        'path': 'request-types-list.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/toefl/edit/', static.serve, kwargs={
        'path': 'request-type-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/add/', static.serve, kwargs={
        'path': 'request-type-form.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/toefl/', static.serve, kwargs={
        'path': 'request-type-description.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/toefl/confirm/', static.serve, kwargs={
        'path': 'request-type-confirm.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('request/history/', static.serve, kwargs={
        'path': 'request-history.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
    path('withdraw/', static.serve, kwargs={
        'path': 'withdraw-request.html', 'document_root': os.path.join(settings.BASE_DIR, 'htmls')}),
]
