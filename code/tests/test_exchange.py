from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest


class ExchangeTest(BaseTest, AmountValidate("output_amount")):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('exchange')

    def findForm(self, form_name="exchange_form"):
        self.form = self.driver.find_element_by_css_selector("form[name='"+form_name+"']")
        self.input_currency = Select(self.driver.find_element_by_id('input_currency'))
        if form_name != "exchange_form":
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

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_big_exchange(self):
        self.findAndFillForm()
        self.output_amount.send_keys('1000000')
        self.submitForm()
        self.assertTrue(int(self.balance_IRR.text) == 100000 and int(self.balance_USD.text) == 100000)

    def test_submit_exchange(self):
        self.findAndFillForm()
        self.submitForm()
        self.findForm("exchange_confirm_form")

    def test_confirm_exchange(self):
        self.findAndFillForm()
        receive_amount = int(self.output_amount.text)
        self.submitForm()
        self.findForm("exchange_confirm_form")
        self.assertTrue(int(self.output_amount.text) == receive_amount)
        pay_amount = int(self.input_amount.text)
        self.submitForm()
        self.balance_IRR = self.driver.find_element_by_id('balance_IRR')
        self.balance_USD = self.driver.find_element_by_id('balance_USD')
        self.assertTrue(int(self.balance_IRR.text) == 100000 - pay_amount and int(self.balance_USD.text) == 100000 + receive_amount)
