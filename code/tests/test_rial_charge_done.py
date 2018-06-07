from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.email_validate import EmailValidate
from tests.utils import createCustomer


class RialChargeRequestTest(BaseTest):

    def setUp(self):
        super(RialChargeRequestTest, self).setUp()
        # TODO: POST SOMETHING TO FAKE BANK DATA
        self.getURL("charge/done")

    def test_result_shown(self):
        self.driver.find_element_by_id("payment-result")






