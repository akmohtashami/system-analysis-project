from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest
from tests.base_django import BaseDjangoTest
from tests.email_validate import EmailValidate


class LoginTest(BaseDjangoTest, EmailValidate("email")):
    def setUp(self):
        super(LoginTest, self).setUp()
        self.getURL(reverse('users:login'))

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='login_form']")
        self.email = self.form.find_element_by_name('username')
        self.password = self.form.find_element_by_name('password')
        self.submit_button = self.form.find_element_by_name('submit')

        self.email.send_keys(self.CUSTOMER_INFO[0][0])
        self.password.send_keys(self.CUSTOMER_INFO[0][1])

    def submitForm(self, find_again=True):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        if find_again:
            self.findAndFillForm()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_login(self):
        self.findAndFillForm()
        self.submitForm(find_again=False)
        self.driver.find_element_by_class_name("success")

    def test_empty_password(self):
        self.findAndFillForm()
        self.password.clear()
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password, "error"))

    def test_invalid_password(self):
        self.findAndFillForm()
        self.password.clear()
        self.password.send_keys("invalid_password")
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password, "error"))

    def test_invalid_email(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys("invalid_email@gmail.com")
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password, "error"))

    def test_invalid_email_and_password(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys("invalid_email@gmail.com")
        self.password.clear()
        self.password.send_keys("invalid_password")
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password, "error"))