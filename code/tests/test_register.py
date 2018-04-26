from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class RegisterTest(BaseTest, EmailValidate("email")):
    def setUp(self):
        super(RegisterTest, self).setUp()
        self.getURL('register')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='register_form']")
        self.name = self.driver.find_element_by_name('name')
        self.email = self.driver.find_element_by_name('email')
        self.password = self.driver.find_element_by_name('password')
        self.password_confirmation = self.driver.find_element_by_name('passwordConfirmation')
        self.submit_button = self.driver.find_element_by_name('submit')

        self.name.send_keys('test')
        self.email.send_keys('test@gmail.com')
        self.password.send_keys('password')
        self.password_confirmation.send_keys('password')

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

    def checkUserRegistered(self):
        pass

    def checkUserNotRegistered(self):
        pass

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_register(self):
        self.findAndFillForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")

    def test_empty_name(self):
        self.findAndFillForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue("error" in self.firstname.get_attribute("class"))

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

    def test_repetitious_email(self):
        self.findAndFillForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")

        self.name.clear()
        self.email.clear()
        self.password.clear()
        self.password_confirmation.clear()

        self.findAndFillForm()
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))
