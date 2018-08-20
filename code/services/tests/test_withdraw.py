from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest
from tests.email_validate import EmailValidate


class WithdrawRequestTestBase(AmountValidate("amount")):

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='request_fill_form']")
        self.amount = self.form.find_element_by_name('amount')
        self.sheba = self.form.find_element_by_name('sheba')
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self):
        self.amount.send_keys("100")
        self.sheba.send_keys("IR062960000000100324200001")

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
        self.driver.find_element_by_css_selector("form[name='confirm_form']")

    def test_invalid_sheba(self):
        self.findAndFillForm()
        self.sheba.clear()
        self.sheba.send_keys('A')
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(self.sheba, "error"))

    def test_empty_sheba(self):
        self.findAndFillForm()
        self.sheba.clear()
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(self.sheba, "error"))

    def test_confirm(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_css_selector("form[name='confirm_form']")
        self.total_due = self.driver.find_element_by_id('due_amount')
        self.form = self.driver.find_element_by_css_selector("form[name='confirm_form']")
        self.submit_button = self.form.find_element_by_name("confirm_button")
        self.total_due = int(self.total_due.text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('confirm_button')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)

        self.assertTrue("history" in self.driver.current_url, "Must be redirected to history")


class WithdrawRequestTestForCustomer(BaseDjangoTest, WithdrawRequestTestBase):
    def setUp(self):
        super(WithdrawRequestTestForCustomer, self).setUp()
        self.loginAsCustomer()
        self.getURL(reverse("services:withdraw"))


class WithdrawRequestTestForAgent(BaseDjangoTest, WithdrawRequestTestBase):
    def setUp(self):
        super(WithdrawRequestTestForAgent, self).setUp()
        self.loginAsAgnet()
        self.getURL(reverse("services:withdraw"))