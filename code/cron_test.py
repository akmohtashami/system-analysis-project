from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

import os

scheduler = BlockingScheduler()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypay.settings")

@scheduler.scheduled_job('interval', minutes=1)
def run_reject_long_waiting_requests():
    call_command("reject_long_waiting_requests")


scheduler.start()