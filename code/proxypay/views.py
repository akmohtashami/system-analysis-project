from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

__all__ = ["IndexView", ]


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "base.html")
        else:
            return HttpResponseRedirect(reverse("users:login"))


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)