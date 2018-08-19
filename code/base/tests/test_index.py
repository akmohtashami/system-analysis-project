from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest


class EditIndexTest(BaseDjangoTest):
    def setUp(self):
        super(EditIndexTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse('edit_index'))

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='edit_index_form']")
        self.index_content = self.driver.find_element_by_name('index_content')
        self.submit_button = self.driver.find_element_by_name('submit')

    def fillForm(self):
        self.index_content.clear()
        self.index_content.send_keys('Hello1')

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()

    def submitForm(self):
        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('submit')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)

    def test_form_inputs(self):
        self.findAndFillForm()

    def test_save(self):
        self.findAndFillForm()
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.getURL(reverse("index"))
        self.assertTrue("Hello1" in self.driver.page_source)

        self.getURL(reverse("edit_index"))
        self.findAndFillForm()
        self.index_content.clear()
        self.index_content.send_keys('Hello2')
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.getURL(reverse("index"))
        self.assertTrue("Hello2" in self.driver.page_source)

    def test_text_multi_line(self):
        self.findAndFillForm()
        old_len = len(self.index_content.get_attribute("value"))
        self.index_content.send_keys(Keys.ENTER)
        self.index_content.send_keys("And the test shall continue")
        new_len = len(self.index_content.get_attribute("value"))
        self.assertNotEqual(old_len, new_len, "Multi-line text must be allowed")

    def test_empty_text(self):
        self.findAndFillForm()
        self.index_content.clear()
        self.submitForm()
        self.driver.find_element_by_class_name("success")
