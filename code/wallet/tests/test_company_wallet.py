from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest


class CompanyWalletTest(BaseDjangoTest, AmountValidate("charge_amount")):
    def setUp(self):
        super(CompanyWalletTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse('wallet:company_wallets'))

    def findForm(self):
        self.rial_balance = self.driver.find_element_by_id('wallet_IRR_balance')
        self.dollar_balance = self.driver.find_element_by_id('wallet_USD_balance')
        self.euro_balance = self.driver.find_element_by_id('wallet_EUR_balance')
        self.form = self.driver.find_element_by_css_selector("form[name='charge_form']")
        self.charge_amount = self.form.find_element_by_name('amount')
        self.submit_button = self.driver.find_element_by_name('submit')

    def fillForm(self):
        self.charge_amount.send_keys('1000')

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('submit')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def test_form_inputs(self):
        self.findForm()

    def test_ok_charge(self):
        self.findAndFillForm()
        current_balance = float(self.rial_balance.text)
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.assertTrue(float(self.rial_balance.text) == current_balance + 1000)
