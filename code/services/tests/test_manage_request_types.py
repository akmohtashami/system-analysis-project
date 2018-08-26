from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.base import SemanticSelect
from tests.base_django import BaseDjangoTest


class ManageRequestTypeTest(BaseDjangoTest):

    def setUp(self):
        super(ManageRequestTypeTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse("services:service_type_list"))

    def wait_until_list_is_gone(self):
        def link_has_gone_stale(driver):
            try:
                self.table.find_element_by_tag_name("tr")
                return False
            except StaleElementReferenceException:
                return True
        self.wait_for(link_has_gone_stale)

    def findForm(self, edit=False):
        if not edit:
            self.form = self.driver.find_element_by_css_selector("form[name='service_type_form']")
            self.short_name = self.form.find_element_by_name("short_name")
        else:
            self.form = self.driver.find_element_by_css_selector("form[name='service_type_details_form']")
        self.name = self.form.find_element_by_name("name")
        self.currency = SemanticSelect(self.form.find_element_by_name("currency"))
        self.fee = self.form.find_element_by_name("fee")
        self.visible = self.form.find_element_by_name("is_active")
        self.description = self.form.find_element_by_name("description")
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self, edit=False):
        if not edit:
            self.short_name.send_keys("toefl")
        self.name.send_keys("TOEFL")
        self.currency.select_by_value("USD")
        self.fee.send_keys("7")
        self.description.send_keys("Some description")
        if not self.visible.is_selected():
            self.visible.click()

    def findAndFillForm(self, edit=False):
        self.findForm(edit)
        self.fillForm(edit)

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

    def findAddForm(self):
        self.findList()
        self.add_link.click()
        self.wait_until_list_is_gone()
        self.findForm()

    def findEditForm(self):
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            try:
                td.find_element_by_tag_name("a").click()
                self.wait_until_list_is_gone()
                found = True
                break
            except:
                pass
        self.assertTrue(found)
        self.findForm(edit=True)

    def findList(self):
        self.add_link = self.driver.find_element_by_name("add_new_type")
        self.table = self.driver.find_element_by_id("service_types")

    def test_list(self):
        self.findList()

    def test_add_submit(self):
        self.findAddForm()
        self.fillForm()
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.getURL(reverse("services:service_type_list"))
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            if "TOEFL" in td.get_attribute('innerHTML'):
                found = True
                break
        self.assertTrue(found)

    def test_visibility_true(self):
        self.findAddForm()
        self.fillForm()
        self.submitForm()
        self.logout()
        self.loginAsCustomer()
        self.getURL(reverse("services:service_description", args=('toefl',)))
        self.assertTrue("Some description" in self.driver.find_element_by_id("description").get_attribute("innerHTML"))

    def test_visibilty_false(self):
        self.findAddForm()
        self.fillForm()
        self.visible.click()
        self.submitForm()
        self.logout()
        self.loginAsCustomer()
        self.getURL(reverse("services:service_description", args=('toefl',)))
        error = False
        try:
            self.driver.find_element_by_id("description")
        except:
            error = True
        self.assertTrue(error)

    def test_edit_submit(self):
        self.findEditForm()
        self.name.clear()
        self.name.send_keys("EDITED")
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.getURL(reverse("services:service_type_list"))
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            if "EDITED" in td.get_attribute('innerHTML'):
                found = True
                break
        self.assertTrue(found)

    def test_short_name_in_add(self):
        self.findAddForm()
        self.fillForm()
        self.short_name.clear()
        self.short_name.send_keys("Aa aa")
        self.submitForm()
        self.findForm()
