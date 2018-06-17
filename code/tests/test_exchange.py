from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.base import BaseTest
from tests.utils import createCustomer


class ExchangeTest(BaseTest, AmountValidate("output_amount")):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        createCustomer('test@gmail.com', 'password', 10000, 0, 0)
        self.login('test@gmail.com', 'password')
        self.getURL('exchange')

    def findForm(self, form_name="exchange_form"):
        self.form = self.driver.find_element_by_css_selector("form[name='"+form_name+"']")
        self.input_currency = Select(self.driver.find_element_by_id('input_currency'))
        self.input_amount = self.driver.find_element_by_id('input_amount')
        self.output_currency = Select(self.driver.find_element_by_id('output_currency'))
        self.output_amount = self.driver.find_element_by_id('output_amount')
        self.submit_button = self.driver.find_element_by_name('submit')

    def fillForm(self):
        self.input_currency.select_by_value('IRR')
        self.output_currency.select_by_value('USD')
        self.output_amount.send_keys('1')

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
        self.findNewAmount()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_exchange(self):
        self.findAndFillForm()
        received = int(self.output_amount.text)
        self.submitForm()
        self.findForm("exchange_confirm_form")
