from django.urls import reverse
from selenium.common.exceptions import StaleElementReferenceException


from tests.amount_validate import AmountValidate
from tests.base import BaseTest
from tests.base_django import BaseDjangoTest
from tests.email_validate import EmailValidate


class RequestHistoryTest(BaseDjangoTest):

    def setUp(self):
        super(RequestHistoryTest, self).setUp()
        self.loginAsCustomer()
        self.getURL(reverse("services:requests_history"))

    def test_history(self):
        history_part = self.driver.find_element_by_id("history")








