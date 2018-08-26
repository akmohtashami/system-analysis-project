from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_django import BaseDjangoTest


class ProcessRequestTest(BaseDjangoTest):
    def setUp(self):
        super(ProcessRequestTest, self).setUp()
        self.loginAsAgnet()
        self.getURL(reverse('services:requests_list'))

    def wait_until_list_is_gone(self):
        def link_has_gone_stale(driver):
            try:
                self.table.get_attribute('innerHTML')
                return False
            except StaleElementReferenceException:
                return True
        self.wait_for(link_has_gone_stale)

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[id='request_details_form']")

    def selectOneRequest(self):
        self.createRequest()
        self.table = self.driver.find_element_by_id("list")
        rows = self.table.find_elements_by_tag_name("tr")
        for tr in rows:
            row = tr.find_elements_by_tag_name("td")
            found = False
            for td in row:
                if 'انتظار' in td.text:
                    found = True
            if not found:
                continue
            for td in row:
                try:
                    td.find_elements_by_tag_name("a").click()
                    self.wait_until_list_is_gone()
                    found = False
                    break
                except:
                    pass
            self.assertTrue(not found)
            self.findForm()
            return
        self.assertTrue(False, 'Free request not found!')

    def findRequestByID(self):
        self.getURL(reverse('services:requests_list'))
        self.createRequest()
        self.table = self.driver.find_element_by_id("requests")
        rows = self.table.find_elements_by_tag_name("tr")
        for tr in rows:
            row = tr.find_elements_by_tag_name("td")
            found = True
            for td in row:
                try:
                    td.find_elements_by_tag_name("a").click()
                    self.wait_until_list_is_gone()
                    found = False
                    break
                except:
                    pass
            self.assertTrue(not found)
            self.findForm()
            return
        self.assertTrue(False, 'Desired request not found!')

    def submitForm(self, button):
        # Not using self.form.submit deliberately
        button.click()

        def form_has_gone_stale(driver):
            try:
                self.driver.find_element_by_id('requests')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def loginWithManager(self):
        self.logout()
        self.loginAsManager()
        self.getURL(reverse('services:requests_list'))

    def test_select_one_request(self):
        self.selectOneRequest()

    def test_ok_accept_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.assertTrue(self.status.text == 'Processing')
        self.form.find_element_by_class_name("success")

    def test_double_accept(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        try:
            self.accept = self.driver.find_element_by_name('accept')
            self.assertTrue(False, 'Double accept is possible')
        except:
            pass

    def test_ok_reject_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.reject = self.driver.find_element_by_name('reject')
        self.submitForm(self.reject)
        self.assertTrue(self.status.text == 'Free')
        self.form.find_element_by_class_name("success")

    def test_Free_reject(self):
        self.selectOneRequest()
        try:
            self.reject = self.driver.find_element_by_name('reject')
            self.assertTrue(False, 'Reject free is possible')
        except:
            pass

    def test_free_done(self):
        self.selectOneRequest()
        try:
            self.accomplish = self.driver.find_element_by_name('accomplish')
            self.assertTrue(False, 'Accomplish free is possible')
        except:
            pass

    def test_ok_accomplish_request(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('accomplish')
        self.submitForm(self.accomplish)
        self.assertTrue(self.status.text == 'Done')
        self.form.find_element_by_class_name("success")

    def test_accomplish_accept(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('accomplish')
        self.submitForm(self.accomplish)
        try:
            self.accept = self.driver.find_element_by_name('accept')
            self.assertTrue(False, 'accept done is possible')
        except:
            pass

    def test_accomplish_reject(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('accomplish')
        self.submitForm(self.accomplish)
        try:
            self.reject = self.driver.find_element_by_name('reject')
            self.assertTrue(False, 'Reject done is possible')
        except:
            pass

    def test_double_accomplish(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('accomplish')
        self.submitForm(self.accomplish)
        try:
            self.accomplish = self.driver.find_element_by_name('accomplish')
            self.assertTrue(False, 'Accomplish done is possible')
        except:
            pass

    def test_reject_others(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.logout()
        self.loginAsAgnet(1)
        self.findRequestByID()
        try:
            self.reject = self.driver.find_element_by_name('reject')
            self.assertTrue(False, 'Reject others request is possible')
        except:
            pass

    def test_accomplish_others(self):
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.logout()
        self.loginAsAgnet(1)
        self.findRequestByID()
        try:
            self.accomplish = self.driver.find_element_by_name('accomplish')
            self.assertTrue(False, 'Accomplish others request is possible')
        except:
            pass

    def test_manager_accept_request(self):
        self.loginWithManager()
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.assertTrue(self.status.text == 'Processing')
        self.form.find_element_by_class_name("success")

    def test_manager_accomplish_request(self):
        self.loginWithManager()
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.accomplish = self.driver.find_element_by_name('accomplish')
        self.submitForm(self.accomplish)
        self.assertTrue(self.status.text == 'Done')
        self.form.find_element_by_class_name("success")

    def test_manager_reject_request(self):
        self.loginWithManager()
        self.selectOneRequest()
        self.accept = self.driver.find_element_by_name('accept')
        self.submitForm(self.accept)
        self.reject = self.driver.find_element_by_name('reject')
        self.submitForm(self.reject)
        self.assertTrue(self.status.text == 'Free')
        self.form.find_element_by_class_name("success")

    def test__accept_request(self):
        self.logout()
        self.loginAsCustomer()
        try:
            self.getURL(reverse('services:requests_list'))
            self.assertTrue(False, 'user can see list of requests.')
        except:
            pass
