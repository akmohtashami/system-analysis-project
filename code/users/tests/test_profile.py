from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException, InvalidElementStateException, \
    NoSuchElementException

from tests.base_django import BaseDjangoTest


class ProfileTest(BaseDjangoTest):
    def setUp(self):
        super(ProfileTest, self).setUp()
        self.loginAsManager()
        self.getURL(reverse("users:users_list"))

    def wait_until_list_is_gone(self):
        def link_has_gone_stale(driver):
            try:
                self.table.find_element_by_tag_name("tr")
                return False
            except StaleElementReferenceException:
                return True
        self.wait_for(link_has_gone_stale)

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='profile_form']")
        self.name = self.form.find_element_by_name('name')
        self.active = self.form.find_element_by_name('is_active')
        self.submit_button = self.form.find_element_by_name('submit')

    def fillForm(self):
        self.name.clear()
        self.name.send_keys('testX')

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
        self.findForm()

    def findList(self):
        self.table = self.driver.find_element_by_id("list")

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

    def test_list(self):
        self.findList()

    def test_update_profile(self):
        self.findEditForm()
        self.fillForm()
        self.submitForm()
        self.driver.find_element_by_class_name("success")
        self.getURL(reverse('users:users_list'))
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found = False
        for td in first_row:
            if "testX" in td.get_attribute('innerHTML'):
                found = True
                break
        self.assertTrue(found)

    def test_empty_name(self):
        self.findEditForm()
        self.name.clear()
        self.submitForm()
        self.findForm()
        self.assertTrue(self.checkHasClass(self.name, 'error'))

    def test_change_email(self):
        self.findEditForm()
        try:
            self.email = self.form.find_element_by_name('email')
            self.email.clear()
            self.assertTrue(False)
        except NoSuchElementException or InvalidElementStateException:
            pass

    def test_change_status(self):
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found1 = False
        for td in first_row:
            if "غیر" in td.get_attribute('innerHTML'):
                found1 = True
                break
        self.findEditForm()
        self.active.click()
        self.submitForm()
        self.getURL(reverse('users:users_list'))
        self.findList()
        first_row = self.table.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")
        found2 = False
        for td in first_row:
            if "غیر" in td.get_attribute('innerHTML'):
                found2 = True
                break
        self.assertTrue(found1 != found2)
