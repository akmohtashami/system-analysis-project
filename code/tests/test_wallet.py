from tests.base import BaseTest


class WalletTest(BaseTest):
    def setUp(self):
        super(WalletTest, self).setUp()
        self.loginAsCustomer()
        self.getURL('wallet')

    def findForm(self):
        self.name = self.driver.find_element_by_id('name')
        self.rial_balance = self.driver.find_element_by_id('rial_balance')
        self.dollar_balance = self.driver.find_element_by_id('dollar_balance')
        self.euro_balance = self.driver.find_element_by_id('euro_balance')

    def test_form_inputs(self):
        self.findForm()
