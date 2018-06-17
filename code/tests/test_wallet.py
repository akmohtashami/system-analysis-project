from tests.base import BaseTest


class ExchangeTest(BaseTest):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('wallet')

    def findForm(self):
        self.name = self.driver.find_element_by_id('name')
        self.balance_IRR = self.driver.find_element_by_id('balance_IRR')
        self.balance_USD = self.driver.find_element_by_id('balance_USD')
        self.balance_EUR = self.driver.find_element_by_id('balance_EUR')

    def test_form_inputs(self):
        self.findForm()
