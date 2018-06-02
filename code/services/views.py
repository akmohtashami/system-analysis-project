from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from services.forms import AddServiceTypeForm


class AddServiceTypeView(View):

    def render_form(self, request, form):
        return render(request, 'services/service-type-form.html', context={
            "form": form
        })

    def get(self, request):
        form = AddServiceTypeForm()
        return self.render_form(request, form)

    def post(self, request):
        form = AddServiceTypeForm(request.POST)
        if form.is_valid():
            messages.success(request, _("New service type has been successfully added."))
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return self.render_form(request, form)
