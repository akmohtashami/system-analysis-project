from django.urls import reverse

from tests.base import BaseTest
from tests.base_django import BaseDjangoTest


class CustomerWalletTest(BaseDjangoTest):
    def setUp(self):
        super(CustomerWalletTest, self).setUp()
        self.loginAsCustomer()
        self.getURL(reverse('wallet:wallets'))

    def findForm(self):
        self.rial_balance = self.driver.find_element_by_id('wallet_IRR_balance')
        self.dollar_balance = self.driver.find_element_by_id('wallet_USD_balance')
        self.euro_balance = self.driver.find_element_by_id('wallet_EUR_balance')

    def test_form_inputs(self):
        self.findForm()


class EmployeeWalletTest(BaseDjangoTest):
    def setUp(self):
        super(EmployeeWalletTest, self).setUp()
        self.loginAsAgnet()
        self.getURL(reverse('wallet:wallets'))

    def findForm(self):
        self.rial_balance = self.driver.find_element_by_id('wallet_IRR_balance')
        with self.assertRaises(Exception):
            self.dollar_balance = self.driver.find_element_by_id('wallet_USD_balance')
        with self.assertRaises(Exception):
            self.euro_balance = self.driver.find_element_by_id('wallet_EUR_balance')

    def test_form_inputs(self):
        self.findForm()


class AdminWalletTest(BaseDjangoTest):
    def setUp(self):
        super(AdminWalletTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse('wallet:wallets'))

    def findForm(self):
        self.rial_balance = self.driver.find_element_by_id('wallet_IRR_balance')
        with self.assertRaises(Exception):
            self.dollar_balance = self.driver.find_element_by_id('wallet_USD_balance')
        with self.assertRaises(Exception):
            self.euro_balance = self.driver.find_element_by_id('wallet_EUR_balance')

    def test_form_inputs(self):
        self.findForm()
