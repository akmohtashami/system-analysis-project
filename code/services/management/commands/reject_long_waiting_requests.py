from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from services.models import ServiceRequest, RequestStatus
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        expired_time = timezone.now() -\
                       timedelta(minutes=settings.AUTO_REJECT_TIMEOUT_MINUTES)
        requests = ServiceRequest.objects.filter(
            creation_date__lt=expired_time,
            status=RequestStatus.REJECTED
        ).all()
        for req in requests:
            req.owner.notify_change_status(req)
        count = ServiceRequest.objects.filter(
            creation_date__lt=expired_time,
            status=RequestStatus.PENDING
        ).update(
            status=RequestStatus.REJECTED
        )
        print("Rejected {} requests".format(count))
