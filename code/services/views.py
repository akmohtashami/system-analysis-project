from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext as _

from base.views import LoginRequiredView
from services.forms import AddServiceTypeForm, MakeRequestForm, WithdrawRequestForm
from services.models import ServiceType, ServiceRequest
from wallet.models import Wallet

__all__ = ["AddServiceTypeView", "ServiceTypeDescriptionView",
           "RequestsHistoryView", "WithdrawRequestView"]


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
            form.save()
            messages.success(request, _("New service type has been successfully added."))
            return HttpResponseRedirect(reverse("services:add_new_type"))
        return self.render_form(request, form)


class ServiceTypeDescriptionView(View):

    form = MakeRequestForm

    def get(self, request, service_name):
        service = get_object_or_404(ServiceType,
                                    short_name=service_name,
                                    is_active=True)
        form = self.form() \
            if service.user_can_make_request(request.user) \
            else None
        return render(request, "services/service_description.html", context={
            "service": service,
            "form": form
        })

    def post(self, request, service_name):
        service = get_object_or_404(ServiceType,
                                    short_name=service_name,
                                    is_active=True)
        if not service.user_can_make_request(request.user):
            return self.http_method_not_allowed(request)
        req = ServiceRequest(service_type=service, owner=request.user,
                             currency=service.currency)
        form = self.form(request.POST, instance=req)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            fee = amount * service.fee / 100.0
            total_due = amount + fee
            if "confirm_button" in request.POST:
                with transaction.atomic():
                    updated = request.user.wallets.filter(
                        currency=service.currency,
                        credit__gte=total_due
                    ).update(
                        credit=F('credit') - total_due
                    )
                    if updated == 0:
                        transaction.set_rollback(True)
                        messages.error(request, _("Insufficient funds"))
                        return HttpResponseRedirect(reverse("services:service_description", kwargs={
                            "service_name": service_name
                        }))
                    if fee > 0:
                        updated = Wallet.get_company_wallets().filter(
                            currency=service.currency
                        ).update(
                            credit=F('credit') + fee
                        )
                        if updated == 0:
                            transaction.set_rollback(True)
                            messages.error(request, _("Internal error. Please try again in a few minutes"))
                            return HttpResponseRedirect(reverse("services:service_description", kwargs={
                                "service_name": service_name
                            }))
                    form.save()
                messages.success(request, _("Your request have been successfully submitted"))
                return HttpResponseRedirect(reverse("services:requests_history"))
            elif "back_button" not in request.POST:
                instance = form.save(commit=False)
                return render(request, "services/service_request_confirm.html", context={
                    "service": service,
                    "form": form,
                    "amount": instance.amount,
                    "description": instance.description,
                    "total_due": total_due
                })
        return render(request, "services/service_description.html", context={
            "service": service,
            "form": form
        })


class RequestsHistoryView(LoginRequiredView):
    def get(self, request):
        return render(request, "services/requests_history.html", context={
            "requests": request.user.requests.all().order_by("-id")
        })


class WithdrawRequestView(ServiceTypeDescriptionView):
    form = WithdrawRequestForm

    def get(self, request):
        return super(WithdrawRequestView, self).get(request, service_name="withdraw")

    def post(self, request):
        return super(WithdrawRequestView, self).post(request, service_name="withdraw")
