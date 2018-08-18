from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest


class SimulateExchangeTestBase():
    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='simulate_exchange_form']")
        self.input_currency = Select(self.driver.find_element_by_name('input_currency'))
        self.input_amount = self.driver.find_element_by_name('input_amount')
        self.output_currency = Select(self.driver.find_element_by_name('output_currency'))
        self.output_amount = self.driver.find_element_by_name('output_amount')
        self.calc_inp_button = self.driver.find_element_by_name('calc_inp')
        self.calc_out_button = self.driver.find_element_by_name('calc_out')

    def fillForm(self):
        self.input_currency.select_by_value('IRR')
        self.output_currency.select_by_value('USD')
        self.input_amount.send_keys('0')
        self.output_amount.send_keys('0')

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()


class SimulateExchangeInputAmountTest(BaseDjangoTest, SimulateExchangeTestBase, AmountValidate('output_amount')):
    def setUp(self):
        super(SimulateExchangeInputAmountTest, self).setUp()
        self.getURL(reverse('wallet:simulate_exchange'))

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.calc_inp_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('calc_inp')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_calculate_input_amount(self):
        self.findAndFillForm()
        self.output_amount.clear()
        self.output_amount.send_keys('1')
        self.submitForm()
        self.assertTrue(float(self.input_amount.get_attribute("value")) != 0)



class SimulateExchangeOutputAmountTest(BaseDjangoTest, SimulateExchangeTestBase, AmountValidate('input_amount')):
    def setUp(self):
        super(SimulateExchangeOutputAmountTest, self).setUp()
        self.getURL(reverse('wallet:simulate_exchange'))

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.calc_out_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('calc_out')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_calculate_output_amount(self):
        self.findAndFillForm()
        self.input_amount.clear()
        self.input_amount.send_keys('10000')
        self.submitForm()
        self.assertTrue(float(self.output_amount.get_attribute("value")) != 0)
