from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from tests.base import BaseTest


class ContactAdminTest(BaseTest):

    def setUp(self):
        super(ContactAdminTest, self).setUp()
        self.getURL("contact")

    def findForm(self):
        self.form = self.driver.find_element_by_xpath("form[name='contact_form']")
        self.name = self.form.find_element_by_name('name')
        self.email = self.form.find_element_by_name('email')
        self.text = self.form.find_element_by_name('text')
        self.submit_button = self.form.find_element_by_name("submit")
        
        self.name.send_keys("Tester")
        self.email.send_keys("test@gmail.com")
        self.text.send_keys("This is a test")

    def test_form_inputs(self):
        self.findForm()

    def test_text_multi_line(self):
        self.findForm()
        old_len = len(self.text.text)
        self.text.send_keys(Keys.ENTER)
        self.text.send_keys("And the test shall continue")
        new_len = len(self.text.text)
        self.assertNotEqual(old_len, new_len, "Multi-line text must be allowed")

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale():
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def test_ok_send(self):
        self.findForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")

    def test_empty_text(self):
        self.findForm()
        self.text.clear()
        self.submitForm()
        self.assertTrue("error" in self.text.get_attribute("class"))

    def test_empty_name(self):
        self.findForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue("error" in self.name.get_attribute("class"))

    def test_empty_email(self):
        self.findForm()
        self.email.clear()
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_at_sign(self):
        self.findForm()
        self.email.clear()
        self.email.send_keys("salam")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_tld(self):
        self.findForm()
        self.email.clear()
        self.email.send_keys("salam@gmail")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))

    def test_invalid_email_no_address(self):
        self.findForm()
        self.email.clear()
        self.email.send_keys("@gmail.com")
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))


