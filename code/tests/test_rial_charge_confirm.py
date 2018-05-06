from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.email_validate import EmailValidate
from tests.utils import createCustomer


class RialChargeRequestTest(BaseTest):

    def setUp(self):
        super(RialChargeRequestTest, self).setUp()
        self.getURL("charge/confirm")

    def test_confirm(self):
        self.form = self.driver.find_element_by_css_selector("form[name='charge_confirm_form']")
        self.email = self.form.find_element_by_id('email')
        self.charge_amount = self.form.find_element_by_id('charge_amount')
        self.due_amount = self.form.find_element_by_id('due_amount')
        self.submit_button = self.form.find_element_by_name("submit")

        self.charge_amount = int(self.charge_amount)
        self.due_amount = int(self.due_amount)

        # Not using self.form.submit deliberately
        self.submit_button.click()

        def form_has_gone_stale(driver):
            try:
                self.form.find_element_by_name('name')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(form_has_gone_stale)

        self.assertTrue("shaparak" in self.driver.current_url, "Must be redirected to shaparak")








