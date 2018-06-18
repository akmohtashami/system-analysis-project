from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class AddMemberTest(BaseTest, EmailValidate('email')):
    def setUp(self):
        super(AddMemberTest, self).setUp()
        self.loginAsManager()
        self.getURL('add_member')

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='register_form']")
        self.name = self.form.find_element_by_name('name')
        self.email = self.form.find_element_by_name('email')
        self.password = self.form.find_element_by_name('password1')
        self.password_confirmation = self.form.find_element_by_name('password2')
        self.member_type = Select(self.form.find_element_by_id('member_type'))
        self.submit_button = self.form.find_element_by_name('submit')

        self.name.send_keys('test')
        self.email.send_keys('test@gmail.com')
        self.password.send_keys('password')
        self.password_confirmation.send_keys('password')
        self.member_type.select_by_value('employee')

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

    def test_repetitious_email(self):
        self.test_ok_register()

        self.getURL('add_member')
        self.findAndFillForm()
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.email, 'error'))