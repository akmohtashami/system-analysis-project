import django
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxypay.settings")
django.setup()

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=5)
def run_reject_long_waiting_requests():
    call_command("reject_long_waiting_requests")


scheduler.start()