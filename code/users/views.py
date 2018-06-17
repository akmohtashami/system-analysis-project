from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import ugettext as _

from users.forms import RegisterForm, LoginForm

__all__ = ["RegisterView", "LoginView", "LogoutView"]


class NotAuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        else:
            return super().dispatch(request, *args, **kwargs)


class RegisterView(NotAuthenticatedView):

    def render_form(self, request, form):
        return render(request, 'users/register.html', context={
            "form": form
        })

    def get(self, request):
        form = RegisterForm()
        return self.render_form(request, form)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("You have been successfully registered."))
            return HttpResponseRedirect(reverse("users:login"))
        return self.render_form(request, form)


class LoginView(NotAuthenticatedView):
    def render_form(self, request, form):
        return render(request, 'users/login.html', context={
            "form": form
        })

    def get(self, request):
        form = LoginForm(request)
        return self.render_form(request, form)

    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            messages.success(request, _("You have been logged in successfully."))
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        return self.render_form(request, form)


class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        messages.success(request, _("You have been logged out successfully."))
        return HttpResponseRedirect(reverse("index"))
