from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View

from base.models import Config
from base.views import LoginRequiredView, AdminRequiredView
from users.models import User
from wallet.forms import RialChargeForm, ExchangeSimulationForm, CompanyRialChargeForm
from wallet.models import Currency, Wallet
from wallet.utils import get_exchange_rates

__all__ = ["MyWalletsView", "CompanyWalletsView",
           "UserRialChargeView", "ExchangeRateView"]


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
            "form": form
        })

    def post(self, request):
        form = RialChargeForm(request.POST)
        if form.is_valid():
            charge_amount = form.cleaned_data["amount"]
            receiver = form.cleaned_data["email"]
            fee = 0  # TODO: Calculate fee
            due_amount = charge_amount * (1 + fee)
            if "confirm_button" in request.POST:
                user, created = User.objects.get_or_create(email=receiver)
                user.wallets.filter(currency=Currency.IRR).update(credit=F('credit') + charge_amount)
                Wallet.get_company_wallets().filter(currency=Currency.IRR).update(credit=F('credit') + fee)
                user.notify_charge(charge_amount)
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
            "form": form
        })


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
            fee = 0  # TODO: Calculate fee
            due_amount = charge_amount * (1 + fee)
            if "confirm_button" in request.POST:
                Wallet.get_company_wallets().filter(currency=Currency.IRR).update(credit=F('credit') + charge_amount)
                messages.success(request, _("Transaction completed successfully"))
                return HttpResponseRedirect(reverse("wallet:company_wallets"))
            elif "back_button" not in request.POST:
                return render(request, "wallet/rial_charge_confirm.html", context={
                    "form": form,
                    "receiver": _("Company"),
                    "charge_amount": charge_amount,
                    "due_amount": due_amount
                })

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



