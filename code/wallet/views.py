from django.shortcuts import render

# Create your views here.
from django.views import View

__all__ = ["MyWalletsView", ]


class MyWalletsView(View):
    def get(self, request):
        return render(request, "wallet/wallet_list.html", context={
            "wallets": request.user.wallets.all()
        })