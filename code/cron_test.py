import django
from apscheduler.schedulers.blocking import BlockingScheduler

from django.core.management import call_command

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypay.settings")
django.setup()

from django.conf import settings

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=settings.AUTO_REJECT_TIMEOUT_MINUTES)
def run_reject_long_waiting_requests():
    call_command("reject_long_waiting_requests")


@scheduler.scheduled_job('cron', day=1)
def run_send_wages():
    call_command("send_wages")

scheduler.start()