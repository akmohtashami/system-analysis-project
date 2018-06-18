from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest


class RegisterWithLinkTest(BaseTest):
    def setUp(self):
        super(RegisterWithLinkTest, self).setUp()
        self.getURL('register_link')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='register_form']")
        self.name = self.form.find_element_by_name('name')
        self.email = self.form.find_element_by_id('email')
        self.password = self.form.find_element_by_name('password1')
        self.password_confirmation = self.form.find_element_by_name('password2')
        self.submit_button = self.form.find_element_by_name('submit')

        self.name.send_keys('test')
        self.password.send_keys('password')
        self.password_confirmation.send_keys('password')

    def submitForm(self, refill=True):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        if refill:
            self.findAndFillForm()

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_ok_register(self):
        self.findAndFillForm()
        self.submitForm(refill=False)
        self.driver.find_element_by_class_name("success")

    def test_empty_name(self):
        self.findAndFillForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.name, 'error'))

    def test_different_password_confirmation(self):
        self.findAndFillForm()
        self.password_confirmation.clear()
        self.password_confirmation.send_keys("password:D")
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.password_confirmation, 'error'))