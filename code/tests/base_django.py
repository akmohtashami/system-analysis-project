from importlib import import_module

from django.conf import settings
from django.test import LiveServerTestCase


from tests.base import BaseTest
from users.models import User, UserType
from wallet.models import Currency
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY


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

    def login(self, username, password):
        user = User.objects.get(email=username)
        assert(user.check_password(password), "Password should be correct")
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        if self.last_url is None:
            self.getURL('/page_404')
        session = SessionStore()
        session[SESSION_KEY] = User.objects.get(email=username).id
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        }

        self.driver.add_cookie(cookie)
        self.driver.refresh()