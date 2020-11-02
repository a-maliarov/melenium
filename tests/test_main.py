# -*- coding: utf-8 -*-

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
from melenium import webdriver
import platform
import unittest
import sys
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

caps = webdriver.ChromeCapabilities('maliarov')
caps.add_argument('--no-sandbox')
caps.add_argument('--headless')

driver = webdriver.ChromeDriver(ChromeDriverManager("86.0.4240.22").install(), desired_capabilities=caps.desired)

class TestMelenium(unittest.TestCase):

    def test_capabilities_add_extension(self):
        caps = webdriver.ChromeCapabilities()
        caps.add_extension(os.path.join(here, 'proxyautologin.crx'))
        self.assertIsNotNone(caps.desired['goog:chromeOptions']['extensions'])

    def test_capabilities_add_argument(self):
        caps = webdriver.ChromeCapabilities()
        caps.add_argument('test')
        self.assertIn('test', caps.desired['goog:chromeOptions']['args'])

    def test_capabilities_add_experimental_option(self):
        chrome_prefs = dict()
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

        caps = webdriver.ChromeCapabilities()
        caps.add_experimental_option(chrome_prefs)
        self.assertEqual(chrome_prefs, caps.desired['goog:chromeOptions']['prefs'])

    def test_capabilities_set_user_agent(self):
        caps = webdriver.ChromeCapabilities()
        caps.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        self.assertIn("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", caps.desired['goog:chromeOptions']['args'])

    def test_capabilities_set_proxy(self):
        caps = webdriver.ChromeCapabilities()
        caps.set_proxy('test')
        self.assertEqual(caps.desired['proxy']['httpProxy'], 'test')

    def test_capabilities_set_download_folder(self):
        caps = webdriver.ChromeCapabilities()
        caps.set_download_folder('test')
        self.assertEqual(caps.desired['goog:chromeOptions']['prefs']['download.default_directory'], 'test')

    def test_capabilities_set_window_size(self):
        caps = webdriver.ChromeCapabilities()
        caps.set_window_size('1920x1080')
        self.assertIn('window-size=1920,1080', caps.desired['goog:chromeOptions']['args'])

    def test_capabilities_from_selenium_options(self):
        chrome_options = Options()
        chrome_options.add_argument('window-size=1920,1080')
        caps = webdriver.ChromeCapabilities.from_selenium_options(chrome_options)
        self.assertIn('window-size=1920,1080', caps.desired['goog:chromeOptions']['args'])

    #-------------------------------------------------------------------------

    def test_chromedriver_find(self):
        driver.get('https://www.amazon.com/errors/validateCaptcha')
        element = driver.find('img')
        self.assertIsNotNone(element)

    def test_chromedriver_find_2(self):
        element = driver.find('input', {'type': 'doesntexist'})
        self.assertIsNone(element)

    def test_chromedriver_find_element_by_bs(self):
        bs_element = BS(driver.page_source, features = 'html.parser').find('img')
        element = driver.find_element_by_bs(bs_element)
        self.assertIsNotNone(element)

    def test_chromedriver_find_element_by_bs_2(self):
        bs_element = BS(driver.page_source, features = 'html.parser').find('input', {'type': 'doesntexist'})
        element = driver.find_element_by_bs(bs_element)
        self.assertIsNone(element)

    def test_chromedriver_wait_for_phrase_in_link(self):
        driver.wait_for.phrase_in_link(10, 'validateCaptcha')
        self.assertIsNotNone(1)

    def test_chromedriver_wait_for_phrase_in_link_2(self):
        driver.wait_for.phrase_in_link(10, 'doesntexist')
        self.assertIsNotNone(1)

    def test_chromedriver_wait_for_element_in_dom(self):
        driver.wait_for.element_in_dom(10, 'div')
        self.assertIsNotNone(1)

    def test_chromedriver_wait_for_element_in_dom_2(self):
        driver.wait_for.element_in_dom(10, 'div', {'class': 'doesntexist'})
        self.assertIsNotNone(1)

#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

#--------------------------------------------------------------------------------------------------------------
