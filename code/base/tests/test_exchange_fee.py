from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest


class ExchangeFeeTest(BaseDjangoTest, AmountValidate("exchange_fee")):
    def setUp(self):
        super(ExchangeFeeTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse('edit_exchange_fee'))

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='exchange_fee_form']")
        self.exchange_fee = self.form.find_element_by_name('exchange_fee')
        self.submit_button = self.form.find_element_by_name('submit')

    def fillForm(self):
        self.exchange_fee.clear()
        self.exchange_fee.send_keys('10')

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

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_submit(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_class_name("success")

    def test_change_exchange_fee(self):
        self.findAndFillForm()
        self.submitForm()
        self.getURL(reverse('edit_exchange_fee'))
        self.findForm()
        self.assertTrue(int(self.exchange_fee.get_attribute('value')) == 10)
