import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from tests.utils import createCustomer, createAgent, createManager, createFreeRequest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseTest(unittest.TestCase):

    CUSTOMER_INFO = [
        ["cust1@system.com", "pass", 100_000, 100_000, 100_000],
    ]

    AGENT_INFO = [
        ["agn1@system.com", "pass", 100_000],
        ["agn2@system.com", "pass", 100_000],
    ]
    MANAGER_INFO = [
        ["mng1@system.com", "pass"],
    ]

    URL_PREFIX = "http://localhost:8001/"

    def setUp(self):
        self.driver = webdriver.Firefox(
            executable_path=os.path.join(
                BASE_DIR,
                'vendor',
                'selenium',
                'geckodriver'
            )
        )
        for customer in self.CUSTOMER_INFO:
            createCustomer(*customer)
        for agent in self.AGENT_INFO:
            createAgent(*agent)
        for manager in self.MANAGER_INFO:
            createManager(*manager)

    def loginAsCustomer(self, id=0):
        self.login(self.CUSTOMER_INFO[id][0], self.CUSTOMER_INFO[id][1])

    def loginAsAgnet(self, id=0):
        self.login(self.AGENT_INFO[id][0], self.AGENT_INFO[id][1])

    def loginAsManager(self, id=0):
        self.login(self.MANAGER_INFO[id][0], self.MANAGER_INFO[id][1])

    def getURL(self, rel_path):
        self.driver.get(self.URL_PREFIX + rel_path)

    def wait_for(self, func, timeout=10):
        WebDriverWait(self.driver, timeout).until(func)

    def login(self, email, password):
        pass

    def logout(self):
        pass

    def createRequest(self):
        createFreeRequest()

    def tearDown(self):
        self.driver.close()
