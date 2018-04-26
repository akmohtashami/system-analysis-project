from selenium.webdriver.common.keys import Keys

from tests.base import BaseTest

class RegisterTest(BaseTest):
    def setUp(self):
        super(RegisterTest, self).setUp()
        self.getURL('register')
        self.assertIn('Register', driver.title)

    def test_register(self):
        self.firstname = self.driver.find_element_by_name('firstname')
        self.lastname = self.driver.find_element_by_name('lastname')
        self.email = self.driver.find_element_by_name('email')
        self.password = self.driver.find_element_by_name('password')
        self.password_confirmation = self.driver.find_element_by_name('passwordConfirmation')
        self.submit = self.driver.find_element_by_name('submit')

        self.firstname.send_keys('peyman')
        self.lastname.send_keys('jabarzade')
        self.email.send_keys('peyman.jabarzade@gmail.com')
        self.password.send_keys('password:D')
        self.password_confirmation.send_keys('password:D')

        submit()
        check_user_registered()

    def test_empty_firstname(self):
        submit = self.driver.find_element_by_name('submit')
        submit.click()
