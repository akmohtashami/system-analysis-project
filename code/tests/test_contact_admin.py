from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class ContactAdminTest(BaseTest, EmailValidate("email")):

    def setUp(self):
        super(ContactAdminTest, self).setUp()
        self.getURL("contact")

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='contact_form']")
        self.name = self.form.find_element_by_name('name')
        self.email = self.form.find_element_by_name('email')
        self.text = self.form.find_element_by_name('text')
        self.submit_button = self.form.find_element_by_name("submit")
        
        self.name.send_keys("Tester")
        self.email.send_keys("test@gmail.com")
        self.text.send_keys("This is a test")

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

    def test_text_multi_line(self):
        self.findAndFillForm()
        old_len = len(self.text.get_attribute("value"))
        self.text.send_keys(Keys.ENTER)
        self.text.send_keys("And the test shall continue")
        new_len = len(self.text.get_attribute("value"))
        self.assertNotEqual(old_len, new_len, "Multi-line text must be allowed")

    def test_ok_send(self):
        self.findAndFillForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")

    def test_empty_text(self):
        self.findAndFillForm()
        self.text.clear()
        self.submitForm()
        self.assertTrue("error" in self.text.get_attribute("class"))

    def test_empty_name(self):
        self.findAndFillForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue("error" in self.name.get_attribute("class"))




