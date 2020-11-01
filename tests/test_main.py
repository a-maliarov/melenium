# -*- coding: utf-8 -*-

from selenium.webdriver.chrome.options import Options
from melenium import webdriver
import unittest
import sys
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

class TestMelenium(unittest.TestCase):

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

    def test_capabilities_add_extension(self):
        caps = webdriver.ChromeCapabilities()
        caps.add_extension(os.path.join(here, 'proxyautologin.crx'))
        self.assertIsNotNone(caps.desired['goog:chromeOptions']['extensions'])

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

#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

#--------------------------------------------------------------------------------------------------------------
