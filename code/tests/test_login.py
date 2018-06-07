from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest
from tests.email_validate import EmailValidate
from tests.utils import createCustomer


class LoginTest(BaseTest, EmailValidate("email")):
    def setUp(self):
        super(LoginTest, self).setUp()
        self.getURL('login')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='login_form']")
        self.email = self.form.find_element_by_name('email')
        self.password = self.form.find_element_by_name('password')
        self.submit_button = self.form.find_element_by_name('submit')

        self.email.send_keys(self.CUSTOMER_INFO[0][0])
        self.password.send_keys(self.CUSTOMER_INFO[0][1])

    def submitForm(self, find_again=False):
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
        redirected = False
        try:
            self.driver.find_element_by_css_selector("form[name='login_form']")
        except:
            redirected = True
            pass
        self.assertTrue(redirected)

    def test_empty_password(self):
        self.findAndFillForm()
        self.password.clear()
        self.submitForm()
        self.assertTrue("error" in self.firstname.get_attribute("class"))

    def test_invalid_password(self):
        self.findAndFillForm()
        self.password.clear()
        self.password.send_keys("invalid_password")
        self.assertTrue("error" in self.password.get_attribute("class"))

    def test_invalid_email(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys("invalid_email@gmail.com")
        self.assertTrue("error" in self.password.get_attribute("class"))

    def test_invalid_email_and_password(self):
        self.findAndFillForm()
        self.email.clear()
        self.email.send_keys("invalid_email@gmail.com")
        self.password.clear()
        self.password.send_keys("invalid_password")
        self.assertTrue("error" in self.password.get_attribute("class"))