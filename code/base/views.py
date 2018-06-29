import markdown
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from base.forms import EditIndexForm
from base.models import Config

__all__ = ["IndexView", "LoginRequiredView", "EmployeeRequiredView", "AdminRequiredView",
           "StaffRequiredView", "CustomerRequiredView", "EditIndexView"]


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin() and not request.user.is_employee():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class EmployeeRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_employee():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_customer():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            index_content = Config.get_solo().index_content
            return render(request, "index.html", context={
                "index_content": markdown.markdown(index_content)
            })
        else:
            return HttpResponseRedirect(reverse("users:login"))


class EditIndexView(AdminRequiredView):

    def render_form(self, request, form):
        return render(request, "edit_index.html", context={
            "form": form
        })

    def get(self, request):
        config = Config.get_solo()
        form = EditIndexForm(instance=config)
        return self.render_form(request, form)

    def post(self, request):
        config = Config.get_solo()
        form = EditIndexForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, _("Home page updated successfully"))
            return HttpResponseRedirect(reverse("edit_index"))
        return self.render_form(request, form)