from tests.base import BaseTest


class ExchangeTest(BaseTest):
    def setUp(self):
        super(ExchangeTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('exchange_rate')

    def findForm(self):
        self.IRR_to_USD = self.driver.find_element_by_id('IRR_to_USD')
        self.IRR_to_EUR = self.driver.find_element_by_id('IRR_to_EUR')
        self.USD_to_IRR = self.driver.find_element_by_id('USD_to_IRR')
        self.EUR_to_IRR = self.driver.find_element_by_id('EUR_to_IRR')

    def test_form_inputs(self):
        self.findForm()
