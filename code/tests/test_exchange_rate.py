from tests.base import BaseTest


class ExchangeRateTest(BaseTest):
    def setUp(self):
        super(ExchangeRateTest, self).setUp()
        self.getURL('exchange_rate')

    def findForm(self):
        self.driver.find_element_by_id('IRR_to_USD')
        self.driver.find_element_by_id('IRR_to_EUR')
        self.driver.find_element_by_id('USD_to_IRR')
        self.driver.find_element_by_id('USD_to_EUR')
        self.driver.find_element_by_id('EUR_to_IRR')
        self.driver.find_element_by_id('EUR_to_USD')

    def test_form_inputs(self):
        self.findForm()
