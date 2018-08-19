from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.amount_validate import AmountValidate
from tests.base_django import BaseDjangoTest
from tests.email_validate import EmailValidate


class RialChargeRequestTest(BaseDjangoTest,
                            EmailValidate("email"),
                            AmountValidate("amount")):

    def setUp(self):
        super(RialChargeRequestTest, self).setUp()
        self.loginAsCustomer()
        self.getURL(reverse("wallet:charge"))

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='charge_form']")
        self.email = self.form.find_element_by_name('email')
        self.amount = self.form.find_element_by_name('amount')
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self):
        self.email.clear()
        self.email.send_keys(self.CUSTOMER_INFO[0][0])
        self.amount.send_keys("20000")

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()

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

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_send(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")

    def processConfirmPage(self):
        self.form = self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")
        self.email = self.driver.find_element_by_id('receiver')
        self.charge_amount = self.driver.find_element_by_id('charge_amount')
        self.due_amount = self.driver.find_element_by_id('total_due')
        self.submit_button = self.form.find_element_by_name("confirm_button")
        self.back_button = self.form.find_element_by_name("back_button")

        self.charge_amount = float(self.charge_amount.text)
        self.due_amount = float(self.due_amount.text)

    def find_confirm_page(self):
        self.findAndFillForm()
        self.submitForm()
        self.processConfirmPage()

    def test_confirm(self):
        self.find_confirm_page()
        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance + self.charge_amount)

    def test_charge_other_existing_user(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys(self.CUSTOMER_INFO[1][0])
        self.submitForm()
        self.processConfirmPage()
        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance)

    def test_charge_other_non_existing_user(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys("oh_my_god_this_can_not_exist@localhost")
        self.submitForm()
        self.processConfirmPage()
        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance)

    def test_cancel(self):
        self.find_confirm_page()

        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.back_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance)

    def test_logged_in_default_email(self):
        self.findForm()
        self.assertEqual(self.email.get_attribute("value"), self.CUSTOMER_INFO[0][0],
                         "Default value for email when charging should be current user")






