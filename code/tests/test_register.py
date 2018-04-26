from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest

class RegisterTest(BaseTest):
    def setUp(self):
        super(RegisterTest, self).setUp()
        self.getURL('register')
        self.assertIn('Register', driver.title)

    def fillForm(self):
        self.firstname = self.driver.find_element_by_name('firstname')
        self.lastname = self.driver.find_element_by_name('lastname')
        self.email = self.driver.find_element_by_name('email')
        self.password = self.driver.find_element_by_name('password')
        self.password_confirmation = self.driver.find_element_by_name('passwordConfirmation')
        self.submit_button = self.driver.find_element_by_name('submit')

        self.firstname.send_keys('firstname')
        self.lastname.send_keys('lastname')
        self.email.send_keys('test@gmail.com')
        self.password.send_keys('password')
        self.password_confirmation.send_keys('password')

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale():
            try:
                self.form.find_element_by_name('firstname')
                return False
            except StaleElementReferenceException:
                return True

    def test_form_inputs(self):
        self.fillForm()

    def test_register(self):
        self.fillForm()
        self.submitForm()
        check_user_registered()

    def test_empty_firstname(self):
        self.fillForm()
        self.firstname.clear()
        self.submitForm()
        self.assertTrue("error" in self.firstname.get_attribute("class"))

    def test_empty_lastname(self):
        self.fillForm()
        self.lastname.clear()
        self.submitForm()
        self.assertTrue("error" in self.lastname.get_attribute("class"))

    def test_empty_email(self):
        self.fillForm()
        self.email.clear()
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_at_sign(self):
        self.fillForm()
        self.email.clear()
        self.email.send_keys("test.com")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_tld(self):
        self.fillForm()
        self.email.clear()
        self.email.send_keys("test@gmail")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_address(self):
        self.fillForm()
        self.email.clear()
        self.email.send_keys("@gmail.com")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_short_password(self):
        self.fillForm()
        self.password.clear()
        self.password_confirmation.clear()
        self.password.send_keys("passw")
        self.password_confirmation.send_keys("passw")
