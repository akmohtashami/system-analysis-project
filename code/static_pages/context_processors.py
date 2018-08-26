from static_pages.models import StaticPage


def available_pages(request):
    return {
        "available_pages": StaticPage.objects.filter(is_visible=True).all()
    }
