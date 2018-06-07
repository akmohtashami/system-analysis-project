from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class ChangePasswordTest(BaseTest):
    def setUp(self):
        super(ChangePasswordTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('change_password')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='change_password_form']")
        self.current_password = self.form.find_element_by_name('current_password')
        self.password = self.form.find_element_by_name('password')
        self.password_confirmation = self.form.find_element_by_name('password_confirmation')
        self.submit_button = self.form.find_element_by_name('submit')

        self.current_password.send_keys(self.CUSTOMER_INFO[0][1])
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
        self.findAndFillForm()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_change_password(self):
        self.findAndFillForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")
        self.logout()
        changedPassword = False
        try:
            self.loginAsCustomer()
        except:
            changedPassword = True
        self.assertTrue(changedPassword)
        self.login(self.CUSTOMER_INFO[0][0], "new_password")

    def test_short_password(self):
        self.findAndFillForm()
        self.password.clear()
        self.password_confirmation.clear()
        self.password.send_keys("passw")
        self.password_confirmation.send_keys("passw")
        self.assertTrue("error" in self.password.get_attribute("class"))

    def test_different_password_confirmation(self):
        self.findAndFillForm()
        self.password_confirmation.clear()
        self.password_confirmation.send_keys("password:D")
        self.assertTrue("error" in self.password_confirmation.get_attribute("class"))

