from django.test import LiveServerTestCase

from tests.base import BaseTest
from users.models import User, UserType
from wallet.models import Currency


class BaseDjangoTest(BaseTest, LiveServerTestCase):
    def getURL(self, rel_path):
        self.driver.get(self.live_server_url + rel_path)

    def createCustomer(self, email, password, rial, dollar, euro):
        user = User.objects.create(name=email, email=email)
        user.set_password(password)
        user.save()
        user.wallets.filter(currency=Currency.IRR).update(credit=rial)
        user.wallets.filter(currency=Currency.USD).update(credit=dollar)
        user.wallets.filter(currency=Currency.EUR).update(credit=euro)

    def createAgent(self, email, password, rial):
        user = User.objects.create(name=email, email=email, type=UserType.Employee)
        user.set_password(password)
        user.save()
        user.wallets.filter(currency=Currency.IRR).update(credit=rial)

    def createManager(self, email, password):
        user = User.objects.create(name=email, email=email, type=UserType.Admin)
        user.set_password(password)
        user.save()