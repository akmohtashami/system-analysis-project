from urllib.parse import urlparse

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View

from base.models import Config
from base.views import LoginRequiredView, AdminRequiredView
from proxypay.settings import SITE_URL
from services.models import ServiceType
from users.models import User
from wallet.forms import RialChargeForm, ExchangeSimulationForm, CompanyRialChargeForm, ExchangeForm, \
    ExchangeConfirmationForm
from wallet.models import Currency, Wallet
from wallet.utils import get_exchange_rates, get_input_from_output_amount
from utils.mail import send_email

__all__ = ["MyWalletsView", "CompanyWalletsView",
           "UserRialChargeView", "ExchangeRateView",
           "CompanyExchangeView", "UserExchangeView"]


class MyWalletsView(LoginRequiredView):
    def get(self, request):
        return render(request, "wallet/wallet_list.html", context={
            "wallets": request.user.wallets.all()
        })


class UserRialChargeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            initial_data = {
                'email': request.user.email
            }
        else:
            initial_data = {}
        form = RialChargeForm(initial=initial_data)
        return render(request, "wallet/rial_charge.html", context={
            "form": form,
            "fee": get_object_or_404(ServiceType,short_name="withdraw").fee
        })

    def post(self, request):
        form = RialChargeForm(request.POST)
        if form.is_valid():
            charge_amount = form.cleaned_data["amount"]
            receiver = form.cleaned_data["email"]
            withdraw = get_object_or_404(ServiceType, short_name="withdraw")
            fee = charge_amount * withdraw.fee / 100.0
            due_amount = charge_amount + fee
            if "confirm_button" in request.POST:
                user, created = User.objects.get_or_create(email=receiver)
                if created:
                    send_email(_("Register in ProxyPay"), _("Your account has been charged %f IRR. Click " % charge_amount) +
                               "<a href=" + SITE_URL + reverse("users:register_with_link", args=(user.link,)) + ">" +
                               _("here") + "</a>" +
                               _(" to register and use your money.")
                               , [user, ])
                user.wallets.filter(currency=Currency.IRR).update(credit=F('credit') + charge_amount)
                Wallet.get_company_wallets().filter(currency=Currency.IRR).update(credit=F('credit') + fee)
                messages.success(request, _("Transaction completed successfully"))
                if user == request.user:
                    return HttpResponseRedirect(reverse("wallet:wallets"))
                else:
                    return HttpResponseRedirect(reverse("wallet:charge"))
            elif "back_button" not in request.POST:
                return render(request, "wallet/rial_charge_confirm.html", context={
                    "form": form,
                    "receiver": receiver,
                    "charge_amount": charge_amount,
                    "due_amount": due_amount
                })

        return render(request, "wallet/rial_charge.html", context={
            "form": form,
            "fee": get_object_or_404(ServiceType,short_name="withdraw").fee
        })


class ExchangeBaseView(View):
    def get(self, request):
        form = ExchangeForm()
        return render(request, "wallet/exchange.html", context={
            "form": form
        })

    def post(self, request):
        ERROR = 3
        if "confirm_button" in request.POST:
            form = ExchangeConfirmationForm(request.POST)
            if not form.is_valid():
                return render(request, "wallet/exchange_confirm.html", context={
                    "form": form,
                    "error": ERROR - 1,
                    "float_format": -ERROR,
                })
                messages.error(request, _("Confirmation failed. Please try again"))
                return HttpResponseRedirect(self.get_failure_redirect_url())
            input_currency = form.cleaned_data["input_currency"]
            output_currency = form.cleaned_data["output_currency"]
            output_amount = form.cleaned_data["output_amount"]
            input_amount = get_input_from_output_amount(
                input_currency,
                output_currency,
                output_amount
            )
            if abs(input_amount - form.cleaned_data["input_amount"]) > (10**(-ERROR)):
                messages.error(request, _("Due to fluctuations in exchange rates "
                                          "we were unable to process your request. "
                                          "Please try again."))
                return HttpResponseRedirect(self.get_failure_redirect_url())

            with transaction.atomic():
                updated = self.get_wallets(request).filter(
                    currency=input_currency,
                    credit__gte=input_amount
                ).update(
                    credit=F('credit') - input_amount
                )
                if updated == 0:
                    transaction.set_rollback(True)
                    messages.error(request, _("Insufficient funds"))
                    return HttpResponseRedirect(self.get_failure_redirect_url())
                updated = self.get_wallets(request).filter(
                    currency=output_currency
                ).update(
                    credit=F('credit') + output_amount
                )
                if updated == 0:
                    transaction.set_rollback(True)
                    messages.error(request, _("Unable to transfer funds"))
                    return HttpResponseRedirect(self.get_failure_redirect_url())
            messages.success(request, _("Exchange completed successfully"))
            return HttpResponseRedirect(self.get_success_redirect_url())
        else:
            form = ExchangeForm(request.POST)
            if "back_button" not in request.POST and form.is_valid():
                input_currency = form.cleaned_data["input_currency"]
                output_currency = form.cleaned_data["output_currency"]
                output_amount = form.cleaned_data["output_amount"]
                input_amount = get_input_from_output_amount(
                    input_currency,
                    output_currency,
                    output_amount
                )
                exchange_data = {
                    "input_currency": input_currency,
                    "output_currency": output_currency,
                    "output_amount": output_amount,
                    "input_amount": input_amount
                }
                confirmation_form = ExchangeConfirmationForm(initial=exchange_data)
                return render(request, "wallet/exchange_confirm.html", context={
                    "form": confirmation_form,
                    "error": ERROR - 1,
                    "float_format": -ERROR,
                    **exchange_data
                })
            return render(request, "wallet/exchange.html", context={
                "form": form
            })

    def get_wallets(self, request):
        raise NotImplementedError

    def get_failure_redirect_url(self):
        raise NotImplementedError

    def get_success_redirect_url(self):
        raise NotImplementedError


class UserExchangeView(LoginRequiredView, ExchangeBaseView):
    def get_wallets(self, request):
        return request.user.wallets.all()

    def get_failure_redirect_url(self):
        return reverse("wallet:exchange")

    def get_success_redirect_url(self):
        return reverse("wallet:wallets")


class CompanyExchangeView(AdminRequiredView, ExchangeBaseView):
    def get_wallets(self, request):
        return Wallet.get_company_wallets()

    def get_failure_redirect_url(self):
        return reverse("wallet:company_exchange")

    def get_success_redirect_url(self):
        return reverse("wallet:company_wallets")


class CompanyWalletsView(AdminRequiredView):
    def get(self, request):
        form = CompanyRialChargeForm()
        company_wallets = Wallet.get_company_wallets()
        return render(request, "wallet/company_wallets.html", context={
            "form": form,
            "wallets": company_wallets
        })

    def post(self, request):
        form = CompanyRialChargeForm(request.POST)
        if form.is_valid():
            charge_amount = form.cleaned_data["amount"]
            Wallet.get_company_wallets().filter(currency=Currency.IRR).update(credit=F('credit') + charge_amount)
            messages.success(request, _("Transaction completed successfully"))
            return HttpResponseRedirect(reverse("wallet:company_wallets"))
        company_wallets = Wallet.get_company_wallets()
        return render(request, "wallet/company_wallets.html", context={
            "form": form,
            "wallets": company_wallets
        })


class ExchangeRateView(View):
    def render_with_form(self, request, form):
        exchange_rates = get_exchange_rates()
        return render(request, "wallet/exchange_rate.html", context={
            "exchange_rates": exchange_rates,
            "fee": Config.get_solo().exchange_fee,
            "form": form
        })

    def get(self, request):
        simulation_form = ExchangeSimulationForm()
        return self.render_with_form(request, simulation_form)

    def post(self, request):
        calculate_first_currency = "calc_inp" in request.POST
        simulation_form = ExchangeSimulationForm(request.POST, calculate_first_currency=calculate_first_currency)
        if simulation_form.is_valid():
            simulation_form = ExchangeSimulationForm(initial=simulation_form.cleaned_data)
        return self.render_with_form(request, simulation_form)



