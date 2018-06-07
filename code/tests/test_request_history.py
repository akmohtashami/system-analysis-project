from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.email_validate import EmailValidate
from tests.utils import createCustomer


class RequestHistoryTest(BaseTest):

    def setUp(self):
        super(RequestHistoryTest, self).setUp()
        self.loginAsCustomer()
        self.getURL("requests/history")

    def test_history(self):
        history_part = self.driver.find_element_by_id("history")








