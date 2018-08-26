from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_django import BaseDjangoTest


class ChangePasswordTest(BaseDjangoTest):
    def setUp(self):
        super(ChangePasswordTest, self).setUp()
        self.loginAsCustomer()
        self.getURL(reverse('users:change_password'))

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='change_password_form']")
        self.password = self.form.find_element_by_name('new_password1')
        self.password_confirmation = self.form.find_element_by_name('new_password2')
        self.submit_button = self.form.find_element_by_name('submit')

        self.password.send_keys('new_password')
        self.password_confirmation.send_keys('new_password')

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

    def test_ok_change_password(self):
        self.findAndFillForm()
        self.submitForm()
        self.logout()
        self.login(self.CUSTOMER_INFO[0][0], "new_password")

    def test_different_password_confirmation(self):
        self.findAndFillForm()
        self.password_confirmation.clear()
        self.password_confirmation.send_keys("password:D")
        self.submitForm()
        self.findAndFillForm()
        self.assertTrue(self.checkHasClass(self.password_confirmation, 'error'))

