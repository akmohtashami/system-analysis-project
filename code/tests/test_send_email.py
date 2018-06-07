from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from tests.base import BaseTest
from tests.email_validate import EmailValidate


class SendEmailTest(BaseTest):

    def setUp(self):
        super(SendEmailTest, self).setUp()
        self.getURL("send-email/")

    def findAndFillForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='email_form']")
        self.title = self.form.find_element_by_name('title')
        self.text = self.form.find_element_by_name('text')
        self.submit_button = self.form.find_element_by_name("submit")
        
        self.title.send_keys("Test")
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

    def test_empty_title(self):
        self.findAndFillForm()
        self.title.clear()
        self.submitForm()
        self.assertTrue("error" in self.title.get_attribute("class"))




