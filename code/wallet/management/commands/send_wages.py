from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import F, Sum, OuterRef, Subquery
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from users.models import User, UserType
from utils.mail import send_email
from wallet.models import Wallet, Currency


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            User.objects.select_for_update()
            total_salary = User.objects.filter(is_active=True).aggregate(Sum('monthly_salary'))['monthly_salary__sum']
            updated = Wallet.get_company_wallets().filter(currency=Currency.IRR, credit__gte=total_salary).update(
                credit=F('credit') - total_salary
            )
            if updated == 0:
                active_admins = User.objects.filter(type=UserType.Admin, is_active=True)
                send_email(
                    _('Salary payment failed'),
                    render_to_string('wallet/low_credit_email.html', context={
                        "total_salary": total_salary
                    }),
                    active_admins
                )
                print("Failed payment of salary due to low credit")
                transaction.set_rollback(True)
                return
            related_user = User.objects.filter(pk=OuterRef("owner_id"))
            updated = Wallet.objects.filter(currency=Currency.IRR, owner__is_active=True).\
                annotate(owner_monthly_salary=Subquery(related_user.values("monthly_salary")[:1])).\
                update(credit=F('credit') + F('owner_monthly_salary'))
            print("Paid salary of {} users. Total paid: {}".format(updated, total_salary))
