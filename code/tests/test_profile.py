from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class ProfileTest(BaseTest, EmailValidate('email')):
    def setUp(self):
        super(ProfileTest, self).setUp()
        self.loginAsManager()
        self.getURL('profile/1')

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='profile_form']")
        self.name = self.form.find_element_by_name('name')
        self.email = self.form.find_element_by_name('email')
        self.status = self.form.find_element_by_id('status')
        self.submit_button = self.form.find_element_by_name('update')
        self.change_status = self.form.find_element_by_name('change_status')

    def fillForm(self):
        self.name.clear()
        self.name.send_keys('testX')
        self.email.clear()
        self.email.send_keys('testX@gmail.com')

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()

    def submitForm(self, refill=True, change_status=False):
        # Not using self.form.submit deliberately
        if change_status:
            self.change_status.click()
        else:
            self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        if refill:
            self.findForm()

    def test_form_inputs(self):
        self.findForm()

    def test_ok_register(self):
        self.findForm()
        self.fillForm()
        self.submitForm(refill=False)
        self.driver.find_element_by_class_name("success")

    def test_empty_name(self):
        self.findForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue(self.checkHasClass(self.name, 'error'))

    def test_change_status(self):
        self.findForm()
        current_status = self.status.text
        self.submitForm(change_status=True)
        self.driver.find_element_by_class_name("success")
        self.assertTrue(self.status.text != current_status)
        self.submitForm(change_status=True)
        self.driver.find_element_by_class_name("success")
        self.assertTrue(self.status.text == current_status)
