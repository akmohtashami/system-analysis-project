from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.base import BaseTest

class ExchangeTest(BaseTest):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        createCustomer('test@gmail.com', 'password', 1000000, 0, 0)
        self.login('test@gmail.com', 'password')
        self.getURL('exchange')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='exchange_form']")
        self.input_currency = Select(self.driver.find_element_by_name('inputCurrency'))
        self.input_amount = self.driver.find_element_by_name('inputAmount')
        self.output_currency = Select(self.driver.find_element_by_name('outputCurrency'))
        self.output_amount = self.driver.find_element_by_name('outputAmount')
        self.submit_button = self.driver.find_element_by_name('submit')

        self.input_currency.select_by_value('IRR')
        self.output_currency.select_by_value('USD')

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findAndFillForm()

    def test_form_inputs(self):
        self.findAndFillForm()
        self.assertTrue(self.input_amount.text == '0' and self.output_amount.text == '0')

    def test_ok_exchange(self):
        self.findAndFillForm()
        self.input_amount.send_keys('1000')
        received = int(self.output_amount.text)
        self.submitForm()
