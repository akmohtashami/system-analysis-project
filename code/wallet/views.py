from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View

from base.views import LoginRequiredView
from users.models import User
from wallet.forms import RialChargeForm
from wallet.models import Currency

__all__ = ["MyWalletsView", "RialChargeView"]


class MyWalletsView(LoginRequiredView):
    def get(self, request):
        return render(request, "wallet/wallet_list.html", context={
            "wallets": request.user.wallets.all()
        })


class RialChargeView(View):
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
            fee = 0 # TODO: Calculate fee
            due_amount = charge_amount * (1 + fee)
            receiver = form.cleaned_data["email"]
            if "confirm_button" in request.POST:
                user, created = User.objects.get_or_create(email=receiver)
                user.wallets.filter(currency=Currency.IRR).update(credit=F('credit') + charge_amount)
                # TODO: Add fee to company account
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