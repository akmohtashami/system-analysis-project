from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select

from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.email_validate import EmailValidate


class ManageStaticPagesTest(BaseTest):

    def setUp(self):
        super(ManageStaticPagesTest, self).setUp()
        self.loginAsManager()
        self.getURL("pages")

    def wait_until_list_is_gone(self):
        def link_has_gone_stale(driver):
            try:
                self.table.find_element_by_tag_name("tr")
                return False
            except StaleElementReferenceException:
                return True
        self.wait_for(link_has_gone_stale)

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='static_page_form']")
        self.short_name = self.form.find_element_by_name("short_name")
        self.name = self.form.find_element_by_name("name")
        self.visible = self.form.find_element_by_name("visible")
        self.description = self.form.find_element_by_name("text")
        self.submit_button = self.form.find_element_by_name("submit")

    def fillForm(self):
        self.short_name.send_keys("static_page")
        self.name.send_keys("static page")
        self.description.send_keys("Some description")

    def findAndFillForm(self):
        self.findForm()
        self.fillForm()

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
        self.findForm()

    def findList(self):
        self.add_link = self.driver.find_element_by_partial_link_text("Add")
        self.table = self.driver.find_element_by_id("request-types")

    def test_list(self):
        self.findList()

    def test_add_submit(self):
        self.findAddForm()
        self.fillForm()
        self.submitForm()
        self.test_list()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            if "static page" in td.get_attribute('innerHTML'):
                found = True
                break
        self.assertTrue(found)

    def test_visibility_true(self):
        self.findAddForm()
        self.fillForm()
        self.submitForm()
        self.getURL("page/static_page")
        self.assertTrue("Some description" in self.driver.find_element_by_id("description").get_attribute("innerHTML"))

    def test_visibilty_false(self):
        self.findAddForm()
        self.fillForm()
        self.visible.click()
        self.submitForm()
        self.getURL("page/static_page")
        error = False
        try:
            self.driver.find_element_by_id("description")
        except:
            error = True
        self.assertTrue(error)

    def test_edit_submit(self):
        self.findEditForm()
        self.assertTrue(len(self.short_name.text) > 0)
        self.assertTrue(len(self.name.text) > 0)
        self.name.clear()
        self.name.send_keys("EDITED")
        self.submitForm()
        self.test_list()
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

    def test_short_name_in_edit(self):
        self.findEditForm()
        self.short_name.clear()
        self.short_name.send_keys("Aa aa")
        self.submitForm()
        self.findForm()

    def test_empty_short_name_in_add(self):
        self.findAddForm()
        self.fillForm()
        self.short_name.clear()
        self.submitForm()
        self.findForm()

    def test_empty_short_name_in_edit(self):
        self.findEditForm()
        self.short_name.clear()
        self.submitForm()
        self.findForm()

    def test_empty_name_in_add(self):
        self.findAddForm()
        self.fillForm()
        self.name.clear()
        self.submitForm()
        self.findForm()

    def test_empty_name_in_edit(self):
        self.findEditForm()
        self.name.clear()
        self.submitForm()
        self.findForm()







