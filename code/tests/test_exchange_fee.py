from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest


class ExchangeTest(BaseTest, AmountValidate("exchange_fee")):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        self.loginAsManager()
        self.getURL('change_exchange_fee')

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='exchange_fee_form']")
        self.exchange_fee = self.driver.find_element_by_id('exchange_fee')
        self.submit_button = self.driver.find_element_by_name('submit')

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

    def test_change_exchange_fee(self):
        self.findAndFillForm()
        self.submitForm()
        self.assertTrue(int(self.exchange_fee.text) == 10)

    def test_invalid_exchange_fee(self):
        self.findAndFillForm()
        self.submitForm()
        self.findAndFillForm()
        self.exchange_fee.clear()
        self.exchange_fee.send_keys('-10')
        self.submitForm()
        self.assertTrue(int(self.exchange_fee.text) == 10)
