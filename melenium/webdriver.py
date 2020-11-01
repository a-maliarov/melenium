# -*- coding: utf-8 -*-

"""
melenium.webdriver
~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ChromeCapabilities']

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup as BS
from selenium.webdriver import *
import pickle
import time

#-----------------------------------------------------------------------------

EMPTY_CAPABILITIES = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',

    'goog:chromeOptions': {
        'prefs': dict(),
        'extensions': list(),
        'args': list()
    },

    'proxy': {
        'httpProxy': None,
        'ftpProxy': None,
        'sslProxy': None,
        'noProxy': None,
        'proxyType': 'MANUAL',
        'class': 'org.openqa.selenium.Proxy',
        'autodetect': False
    }
}

MALIAROV_BASIC_PRESET = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',

    'goog:chromeOptions': {
        'prefs': dict(),
        'extensions': list(),
        'args': [
            'disable-auto-reload',
            'log-level=2',
            'disable-notifications',
            'start-maximized',
            'lang=en',
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"'
        ]
    },

    'proxy': {
        'httpProxy': None,
        'ftpProxy': None,
        'sslProxy': None,
        'noProxy': None,
        'proxyType': 'MANUAL',
        'class': 'org.openqa.selenium.Proxy',
        'autodetect': False
    }
}

presets = {
    'empty': EMPTY_CAPABILITIES,
    'maliarov': MALIAROV_BASIC_PRESET
}

#-----------------------------------------------------------------------------

class ChromeCapabilities(object):

    def __init__(self, preset='empty'):
        if isinstance(preset, str):
            self.desired = presets[preset].copy()
        elif isinstance(preset, dict):
            self.desired = preset.copy()

    def add_argument(self, argument):
        self.desired['goog:chromeOptions']['args'].append(argument)

    def add_experimental_option(self, experimental_option):
        self.desired['goog:chromeOptions']['prefs'] = experimental_option

    def add_extension(self, extension):
        chrome_options = Options()
        chrome_options.add_extension(extension)
        selenium_capabilities = chrome_options.to_capabilities()

        self.desired['goog:chromeOptions']['extensions'].append(selenium_capabilities['goog:chromeOptions']['extensions'][0])

    def set_user_agent(self, user_agent):
        self.add_argument('user-agent={}'.format(user_agent))

    def set_proxy(self, proxy):
        proxy_types_list = ['httpProxy', 'ftpProxy', 'sslProxy']

        for type in proxy_types_list:
            self.desired['proxy'][type] = proxy

    def set_download_folder(self, folder_path):
        self.desired['goog:chromeOptions']['prefs']['download.default_directory'] = folder_path

    def set_window_size(self, window_size):
        self.add_argument('window-size={}'.format(window_size.replace("x", ",")))

    @classmethod
    def from_selenium_options(cls, selenium_options):
        current_options = selenium_options.to_capabilities()
        return cls(current_options)

#-----------------------------------------------------------------------------

# def get_xpath(element):
#
#     def get_index(el):
#         prev_sibs = [tag for tag in el.previous_siblings if tag.name == el.name]
#         next_sibs = [tag for tag in el.next_siblings if tag.name == el.name]
#
#         if (len(prev_sibs) != 0) and (len(next_sibs) != 0):
#             result = '[' + str(len(prev_sibs) + 1) + ']'
#         elif (len(prev_sibs) == 0) and (len(next_sibs) != 0):
#             result = '[1]'
#         elif (len(prev_sibs) != 0) and (len(next_sibs) == 0):
#             result = '[' + str(len(prev_sibs) + 1) + ']'
#         elif (len(prev_sibs) == 0) and (len(next_sibs) == 0):
#             result = ''
#         else:
#             result = ''
#
#         return result
#
#     xpath = ''
#     current_element = element
#     while current_element.name != 'html':
#         xpath = '/' + current_element.name + get_index(current_element) + xpath
#         current_element = current_element.parent
#
#     return '/html' + xpath
#
# class ChromeDriver(webdriver.Chrome):
#
#     def wait_for_element_in_dom(self, *argv, **kwargs):
#         counter = 0
#         while BS(self.page_source, features = 'html.parser').find(*argv, **kwargs) == None:
#             time.sleep(1)
#             counter += 1
#             if counter == 60:
#                 return None
#
#     def wait_for_phrase_in_link(self, phrase, timeout = 60):
#         counter = 0
#         while phrase not in self.current_url:
#             time.sleep(1)
#             counter += 1
#             if counter == timeout:
#                 return None
#
#     def advanced_find(self, *argv, **kwargs):
#         html_element = BS(self.page_source, features = 'html.parser').find(*argv, **kwargs)
#         if html_element != None:
#             xpath = get_xpath(html_element)
#             return self.find_element_by_xpath(xpath)
#         else:
#             return None
#
#     def find_element_by_html(self, html_element):
#         if html_element != None:
#             xpath = get_xpath(html_element)
#             return self.find_element_by_xpath(xpath)
#         else:
#             return None
#
#     def upload_cookies(self, cookies_file):
#         for cookie in pickle.load(open(cookies_file, "rb")):
#             if 'expiry' in cookie:
#                 del cookie['expiry']
#             self.add_cookie(cookie)
#
#     @classmethod
#     def from_scratch(cls):
#         # Downloads webdriver
#         pass
#
#     @staticmethod
#     def click_ignoring_interception(element):
#         while True:
#             try:
#                 element.click()
#                 break
#             except ElementClickInterceptedException:
#                 time.sleep(0.1)
#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------
