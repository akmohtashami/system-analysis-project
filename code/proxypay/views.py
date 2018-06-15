from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

__all__ = ["IndexView", ]


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            raise PermissionDenied
        else:
            return HttpResponseRedirect(reverse("users:login"))