from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.email_validate import EmailValidate


class RialChargeRequestTest(BaseTest,
                            EmailValidate("email"),
                            AmountValidate("amount")):

    def setUp(self):
        super(RialChargeRequestTest, self).setUp()
        self.loginAsCustomer()
        self.getURL("charge")

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='charge_form']")
        self.email = self.form.find_element_by_name('email')
        self.amount = self.form.find_element_by_name('amount')
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self):
        self.email.send_keys("test@gmail.com")
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

    def find_confirm_page(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")
        self.form = self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")
        self.email = self.form.find_element_by_id('email')
        self.charge_amount = self.form.find_element_by_id('charge_amount')
        self.due_amount = self.form.find_element_by_id('due_amount')
        self.submit_button = self.form.find_element_by_name("submit")
        self.back_button = self.form.find_element_by_name("back")

        self.charge_amount = int(self.charge_amount.text)
        self.due_amount = int(self.due_amount.text)

    def test_confirm(self):
        self.find_confirm_page()

        current_irr_balance = int(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = int(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance + self.charge_amount)

    def test_cancel(self):
        self.find_confirm_page()

        current_irr_balance = int(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.back_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        new_irr_balance = int(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance)

    def test_logged_in_default_email(self):
        email = "test@test.ir"
        self.createCustomer(email, "pass1", 0, 0, 0)
        self.login(email, "pass1")
        self.findForm()
        self.assertEqual(self.email.text, email,
                         "Default value for email when charging should be current user")






