from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext as _

from users.forms import RegisterForm

__all__ = ["RegisterView"]


class RegisterView(View):

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
            messages.success(request, _("You have been successfully registered."))
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return self.render_form(request, form)
