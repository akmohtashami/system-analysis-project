import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseTest(unittest.TestCase):

    URL_PREFIX = "http://localhost:8000/"

    def setUp(self):
        self.driver = webdriver.Firefox(
            executable_path=os.path.join(
                BASE_DIR,
                'vendor',
                'selenium',
                'geckodriver'
            )
        )

    def getURL(self, rel_path):
        self.driver.get(self.URL_PREFIX + rel_path)

    def wait_for(self, func, timeout=10):
        WebDriverWait(self.driver, timeout).until(func)

    def login(self, email, password):
        pass

    def tearDown(self):
        self.driver.close()