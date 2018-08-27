from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext as _

from base.views import LoginRequiredView, StaffRequiredView, AdminRequiredView
from proxypay.settings import SITE_URL
from services.forms import AddServiceTypeForm, MakeRequestForm, WithdrawRequestForm, ServiceTypeDetailsForm
from services.models import ServiceType, ServiceRequest, RequestStatus
from users.models import User, UserType
from utils.mail import send_email
from wallet.forms import ReportForm
from wallet.models import Wallet

__all__ = ["AddServiceTypeView", "ServiceTypeDescriptionView", "RequestsHistoryView", "WithdrawRequestView",
           "RequestsListView", "RequestDetailsView", "ServiceTypeListView", "ServiceTypeDetailsView", "ReportView"]


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
            "form": form,
            "currency": service.currency,
            "fee": service.fee
        })

    def post(self, request, service_name):
        service = get_object_or_404(ServiceType,
                                    short_name=service_name,
                                    is_active=True)
        if not service.user_can_make_request(request.user):
            return self.http_method_not_allowed(request)
        req = ServiceRequest(service_type=service, owner=request.user)
        form = self.form(request.POST, instance=req)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            if service.min_amount is not None and service.min_amount > amount:
                form.add_error("amount",
                               _("Amount can not be less than %(amount)s" % {"amount": str(service.min_amount)}))
            elif service.max_amount is not None and service.max_amount < amount:
                form.add_error("amount",
                               _("Amount can not be more than %(amount)s" % {"amount": str(service.max_amount)}))
            else:
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
            "requests": request.user.requests.all().order_by("-creation_date")
        })


class WithdrawRequestView(ServiceTypeDescriptionView):
    form = WithdrawRequestForm

    def get(self, request):
        return super(WithdrawRequestView, self).get(request, service_name="withdraw")

    def post(self, request):
        return super(WithdrawRequestView, self).post(request, service_name="withdraw")


class RequestsListView(StaffRequiredView):
    def get(self, request):
        return render(request, "services/requests_list.html", context={
            "requests": ServiceRequest.objects.order_by("-id"),
            "user": request.user,
            "is_done": RequestStatus.DONE
        })


class RequestDetailsView(StaffRequiredView):

    def get(self, request, link):
        service_request = get_object_or_404(ServiceRequest, link=link)
        service = service_request.service_type

        return render(request, "services/request_details.html", context={
            "service": service,
            "service_request": service_request,
            "is_pending": service_request.status == RequestStatus.PENDING and request.user.is_employee(),
            "is_processing": service_request.status == RequestStatus.PROCESSING and
                             service_request.operator == request.user and request.user.is_employee(),
            "is_done": service_request.status == RequestStatus.DONE and service_request.operator != request.user and
                       (request.user.is_employee() or request.user.is_admin())
        })

    def post(self, request, link):
        service_request = get_object_or_404(ServiceRequest,
                                            link=link)
        if "accept_button" in request.POST:
            if service_request.status != RequestStatus.PENDING or not request.user.is_employee():
                messages.error(request, _("You can't accept this request."))
                return HttpResponseRedirect(reverse("services:details", kwargs={
                    "link": service_request.link
                    }))
            service_request.status = RequestStatus.PROCESSING
            service_request.operator = request.user
            service_request.save(force_update=True)
            service_request.owner.notify_change_status(service_request)
            return HttpResponseRedirect(reverse("services:details", kwargs={
                "link": service_request.link
                }))

        elif "reject_button" in request.POST:
            if service_request.status != RequestStatus.PROCESSING or service_request.operator != request.user:
                messages.error(request, _("You can't reject this request."))
                return HttpResponseRedirect(reverse("services:details", kwargs={
                    "link": service_request.link
                    }))
            service_request.status = RequestStatus.PENDING
            service_request.operator = None
            service_request.save(force_update=True)
            service_request.owner.notify_change_status(service_request)
            return HttpResponseRedirect(reverse("services:details", kwargs={
                "link": service_request.link
                }))

        elif "finish_button" in request.POST:
            if service_request.status != RequestStatus.PROCESSING or service_request.operator != request.user:
                messages.error(request, _("You can't finish this request."))
                return HttpResponseRedirect(reverse("services:details", kwargs={
                    "link": service_request.link
                    }))
            service_request.status = RequestStatus.DONE
            service_request.save(force_update=True)
            service_request.owner.notify_change_status(service_request)
            return HttpResponseRedirect(reverse("services:details", kwargs={
                "link": service_request.link
                }))

        elif "report_button" in request.POST:
            if service_request.status != RequestStatus.DONE or service_request.operator == request.user:
                messages.error(request, _("You can't report this request."))
                return HttpResponseRedirect(reverse("services:details", kwargs={
                    "link": service_request.link
                }))
            return HttpResponseRedirect(reverse("services:report", args=(service_request.link, )))


class ServiceTypeListView(AdminRequiredView):
    def get(self, request):
        return render(request, "services/service_type_list.html", context={
            "services": ServiceType.objects.all().order_by("-name").reverse()
        })


class ServiceTypeDetailsView(AdminRequiredView):
    def render_form(self, request, form, service):
        return render(request, 'services/service_type_details.html', context={
            "form": form,
            "service": service
        })

    def get(self, request, service_name):
        service = get_object_or_404(ServiceType, short_name=service_name)
        form = ServiceTypeDetailsForm(initial={
            'name': service.name,
            'currency': service.currency,
            'fee': service.fee,
            'description': service.description,
            'min_amount': service.min_amount,
            'max_amount': service.max_amount,
            'is_active': service.is_active
        })
        return self.render_form(request, form, service)

    def post(self, request, service_name):
        service = get_object_or_404(ServiceType, short_name=service_name)
        form = ServiceTypeDetailsForm(request.POST, instance=service)
        if form.is_valid():
            form.update(service)
            messages.success(request, _("Service type has been updated."))
            return HttpResponseRedirect(reverse("services:service_type_details", args=(service_name,)))
        return self.render_form(request, form, service)


class ReportView(View):
    def render_form(self, request, form, link):
        return render(request, 'send-email.html', context={
            "form": form
        })

    def get(self, request, link):
        form = ReportForm()
        return self.render_form(request, form, link)

    def post(self, request, link):
        form = ReportForm(request.POST)
        if form.is_valid():
            active_admins = User.objects.filter(type=UserType.Admin).filter(is_active=True)

            if (send_email(_('Report'),
                           render_to_string('services/email.html', context={"name": request.user.name,
                                                                         "email": request.user.email,
                                                                         "text": request.POST['text'],
                                                                          "req_url": SITE_URL + reverse("services:details", args=(link,))}),
            active_admins)):
                messages.success(request, _('Your report has been send successfully.'))
            else:
                messages.warning(request, _('Your report has not been send.'))
            next = request.GET.get("next", request.POST.get("next", reverse("services:details", args=(link,))))
            return HttpResponseRedirect(next)
        return self.render_form(request, form, link)
