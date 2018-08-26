from wallet.models import Wallet


def company_wallets(request):
    if request.user.is_authenticated and request.user.is_admin():
        return {
            "company_wallets": Wallet.get_company_wallets()
        }
    else:
        return {}