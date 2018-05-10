from selenium.common.exceptions import StaleElementReferenceException

from tests.base import BaseTest

class ProcessRequestTest(BaseTest):
    def setUp(self):
        super(ProcessRequestTest, self).setUp()
        self.loginAsAgnet()
        self.getURL('handle-request')

    def findForm(self):
        self.form = self.driver.find_element_by_css_selector("form[id='charge_status_form']")
        self.name = self.driver.find_element_by_id('name')
        self.time = self.driver.find_element_by_id('time')
        self.request_type = self.driver.find_element_by_id('request_type')
        self.payment = self.driver.find_element_by_id('payment')
        self.currency = self.driver.find_element_by_id('currency')
        self.status = self.driver.find_element_by_id('status')

        self.accept = self.driver.find_element_by_name('accept')
        self.reject = self.driver.find_element_by_name('reject')
        self.accomplish = self.driver.find_element_by_name('accomplish')

    def selectOneRequest(self):
        rows = self.table.find_elements_by_tag_name("tr")
        for tr in rows:
            row = tr.find_element_by_tag_name("td")
            found = False
            for td in row:
                try:
                    td.find_element_by_tag_name("a").click()
                    self.wait_until_list_is_gone()
                    found = True
                    break
                except:
                    pass
            self.assertTrue(found)
            self.findForm()
            if self.status.text == 'free':
                return
        self.assertTrue(False, 'free request not found!')

    def submitForm(self, button):
        # Not using self.form.submit deliberately
        button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)
        self.findForm()

    def test_select_one_request(self):
        self.driver.find_element_by_id('requests')
        self.selectOneRequest()

    def test_ok_accept_request(self):
        self.selectOneRequest()
        self.driver.execute_script("arguments[0].innerText = 'free'", self.status)
        self.submitForm(self.accept)
        self.assertTrue(self.status.text == 'processing')
        self.form.find_element_by_class_name("success")

    def test_ok_reject_request(self):
        self.selectOneRequest()
        self.driver.execute_script("arguments[0].innerText = 'processing'", self.status)
        self.submitForm(self.reject)
        self.assertTrue(self.status.text == 'free')
        self.form.find_element_by_class_name("success")

    def test_ok_accomplish_request(self):
        self.selectOneRequest()
        self.driver.execute_script("arguments[0].innerText = 'processing'", self.status)
        self.submitForm(self.accomplish)
        self.assertTrue(self.status.text == 'done')
        self.form.find_element_by_class_name("success")










    def test_empty_name(self):
        self.findForm()
        self.name.clear()
        self.submitForm()
        self.assertTrue("error" in self.firstname.get_attribute("class"))

    def test_short_password(self):
        self.findForm()
        self.password.clear()
        self.password_confirmation.clear()
        self.password.send_keys("passw")
        self.password_confirmation.send_keys("passw")
        self.assertTrue("error" in self.password.get_attribute("class"))

    def test_different_password_confirmation(self):
        self.findForm()
        self.password_confirmation.clear()
        self.password_confirmation.send_keys("password:D")
        self.assertTrue("error" in self.password_confirmation.get_attribute("class"))

    def test_repetitious_email(self):
        self.findForm()
        self.submitForm()
        self.form.find_element_by_class_name("success")

        self.name.clear()
        self.email.clear()
        self.password.clear()
        self.password_confirmation.clear()

        self.findForm()
        self.submitForm()
        self.assertTrue("error" in self.email.get_attribute("class"))