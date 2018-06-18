from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest


class ExchangeTest(BaseTest, AmountValidate("output_amount")):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('exchange')

    def findConfirmationForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='exchange_confirm_form']")
        self.input_currency = self.driver.find_element_by_id('input_currency')
        self.input_amount = self.driver.find_element_by_id('input_amount')
        self.output_currency = self.driver.find_element_by_id('output_currency')
        self.output_amount = self.driver.find_element_by_id('output_amount')
        self.submit_button = self.driver.find_element_by_name('submit')
        self.cancel_button = self.driver.find_element_by_name('cancel')

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='exchange_form']")
        self.input_currency = Select(self.driver.find_element_by_id('input_currency'))
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

    def submitForm(self, cancel=False):
        # Not using self.form.submit deliberately
        if cancel:
            self.cancel_button.click()
        else:
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

    def test_exchange_more_than_balance(self):
        self.findAndFillForm()
        self.output_amount.send_keys('1000000')
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.output_amount, 'error'))

    def test_submit_exchange(self):
        self.findAndFillForm()
        self.submitForm()
        self.findConfirmationForm()

    def test_confirm_exchange(self):
        self.findAndFillForm()
        receive_amount = float(self.output_amount.text)
        self.submitForm()
        self.findConfirmationForm()
        self.assertTrue(float(self.output_amount.text) == receive_amount)
        pay_amount = float(self.input_amount.text)
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        balance_IRR = self.driver.find_element_by_id('balance_IRR')
        balance_USD = self.driver.find_element_by_id('balance_USD')
        self.assertTrue(float(balance_IRR.text) == 100000 - pay_amount and
                        float(balance_USD.text) == 100000 + receive_amount)

    def test_cancel_confirm_exchange(self):
        current_balance = float(self.driver.find_element_by_id('balance_IRR').text)
        self.findAndFillForm()
        self.submitForm()
        self.findConfirmationForm()
        self.submitForm(cancel=True)
        self.driver.find_element_by_class_name("success")
        self.assertTrue(float(self.driver.find_element_by_id('balance_IRR').text) == current_balance)
