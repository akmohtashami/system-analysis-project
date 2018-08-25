from services.models import ServiceType


def available_services(request):
    return {
        "available_services": ServiceType.objects.filter(is_active=True).exclude(short_name='withdraw').all() if request.user.is_authenticated and request.user.is_customer() else None,
        "withdraw_available": ServiceType.objects.filter(short_name='withdraw', is_active=True).exists()
    }