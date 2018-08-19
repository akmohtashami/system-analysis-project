from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from services.models import ServiceType
from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest
from wallet.models import Currency


class MakeRequestTest(BaseDjangoTest, AmountValidate("amount")):

    def setUp(self):
        super(MakeRequestTest, self).setUp()
        self.loginAsCustomer()
        ServiceType.objects.create(
            short_name="toefl",
            name="TOEFL",
            currency=Currency.IRR,
        )
        self.getURL(reverse("services:service_description", kwargs={
            "service_name": "toefl"
        }))

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='request_fill_form']")
        self.amount = self.form.find_element_by_name('amount')
        self.text = self.form.find_element_by_name('description')
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self):
        self.amount.send_keys("100")
        self.text.send_keys("Some Description.")

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

    def findConfirmPage(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_css_selector("form[name='confirm_form']")
        self.total_due = self.driver.find_element_by_id('due_amount')
        self.form = self.driver.find_element_by_css_selector("form[name='confirm_form']")
        self.submit_button = self.form.find_element_by_name("confirm_button")
        self.back_button = self.form.find_element_by_name("back_button")
        self.total_due = int(self.total_due.text)

    def test_confirm(self):
        self.findConfirmPage()
        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('confirm_button')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)

        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance - self.total_due)

    def test_cancel(self):
        self.findConfirmPage()
        current_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)

        # Not using self.form.submit deliberately
        self.back_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('back_button')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)

        new_irr_balance = float(self.driver.find_element_by_id("balance_IRR").text)
        self.assertTrue(new_irr_balance == current_irr_balance)

    def test_text_multi_line(self):
        self.findAndFillForm()
        old_len = len(self.text.get_attribute("value"))
        self.text.send_keys(Keys.ENTER)
        self.text.send_keys("And the test shall continue")
        new_len = len(self.text.get_attribute("value"))
        self.assertNotEqual(old_len, new_len, "Multi-line text must be allowed")

    def test_allow_empty_text(self):
        self.findAndFillForm()
        self.text.clear()
        self.submitForm()
        self.driver.find_element_by_css_selector("form[name='confirm_form']")

