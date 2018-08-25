import os
import unittest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseTest(unittest.TestCase):

    CUSTOMER_INFO = [
        ["cust1@system.com", "pass", 100000, 100000, 100000],
        ["cust2@system.com", "pass", 100000, 100000, 100000],
    ]

    AGENT_INFO = [
        ["agn1@system.com", "pass", 100000],
        ["agn2@system.com", "pass", 100000],
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
            self.createCustomer(*customer)
        for agent in self.AGENT_INFO:
            self.createAgent(*agent)
        for manager in self.MANAGER_INFO:
            self.createManager(*manager)
        self.last_url = None

    def loginAsCustomer(self, id=0):
        self.login(self.CUSTOMER_INFO[id][0], self.CUSTOMER_INFO[id][1])

    def loginAsAgnet(self, id=0):
        self.login(self.AGENT_INFO[id][0], self.AGENT_INFO[id][1])

    def loginAsManager(self, id=0):
        self.login(self.MANAGER_INFO[id][0], self.MANAGER_INFO[id][1])

    def getURL(self, rel_path):
        self.last_url = rel_path
        self.driver.get(self.URL_PREFIX + rel_path)

    def wait_for(self, func, timeout=10):
        WebDriverWait(self.driver, timeout).until(func)

    def login(self, email, password):
        pass

    def logout(self):
        pass

    def createRequest(self):
        pass

    def createCustomer(self, email, password, rial, dollar, euro):
        pass

    def createAgent(self, email, password, rial):
        pass

    def createManager(self, email, password):
        pass

    def checkHasClass(self, elem, class_name):
        while elem != self.driver.find_element_by_tag_name("html"):
            if class_name in elem.get_attribute("class"):
                return True
            elem = elem.find_element_by_xpath("..")

        return False

    def tearDown(self):
        self.driver.close()


class SemanticSelect(object):
    def __init__(self, obj):
        self.obj = obj.find_element_by_xpath("..")

    def select_by_value(self, value):
        self.obj.click()
        self.obj.find_element_by_css_selector("[data-value={}]".format(value)).click()