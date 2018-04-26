import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BaseUnitTest(unittest.TestCase):

    URL_PREFIX = "http://localhost/"

    def setUp(self):
        self.driver = webdriver.Firefox()

    def getURL(self, rel_path):
        self.driver.get(self.URL_PREFIX + rel_path)

    def tearDown(self):
        self.driver.close()