# -*- coding: utf-8 -*-

"""
melenium.webdriver
~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ChromeCapabilities', 'ChromeDriver']

from selenium.webdriver.chrome.options import Options
from selenium.webdriver import *
import pyaction as pa
import pickle
import time

try:
    from bs4 import BeautifulSoup as BS
except ImportError:
    from beautifulsoup4 import BeautifulSoup as BS

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

    # @property
    # def extensions(self):
    #     """
    #     Returns a list of encoded extensions that will be loaded into chrome
    #
    #     """
    #     encoded_extensions = []
    #     for ext in self._extension_files:
    #         file_ = open(ext, 'rb')
    #         # Should not use base64.encodestring() which inserts newlines every
    #         # 76 characters (per RFC 1521).  Chromedriver has to remove those
    #         # unnecessary newlines before decoding, causing performance hit.
    #         encoded_extensions.append(base64.b64encode(file_.read()).decode('UTF-8'))
    #
    #         file_.close()
    #     return encoded_extensions + self._extensions

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

class ChromeDriver(Chrome):

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):

        """
        Creates a new instance of the chrome driver.

        Starts the service and then creates new instance of chrome driver.

        :Args:
         - executable_path - path to the executable. If the default is used it assumes the executable is in the $PATH
         - port - port you would like the service to run, if left as 0, a free port will be found.
         - options - this takes an instance of ChromeOptions
         - service_args - List of args to pass to the driver service
         - desired_capabilities - Dictionary object with non-browser specific
           capabilities only, such as "proxy" or "loggingPref".
         - service_log_path - Where to log information from the driver.
         - chrome_options - Deprecated argument for options
         - keep_alive - Whether to configure ChromeRemoteConnection to use HTTP keep-alive.
        """

        super().__init__(executable_path, port, options, service_args, desired_capabilities, service_log_path, chrome_options, keep_alive)
        self._wait_for = WaitFor(self)

    def find(self, *argv, **kwargs):
        bs_element = BS(self.page_source, features = 'html.parser').find(*argv, **kwargs)

        if bs_element != None:
            xpath = pa.get_xpath(bs_element)
            return self.find_element_by_xpath(xpath)

        else:
            return None

    def find_element_by_bs(self, bs_element):
        if bs_element != None:
            xpath = pa.get_xpath(bs_element)
            return self.find_element_by_xpath(xpath)

        else:
            return None

    def upload_cookies(self, cookies_file, exclude=['expiry']):
        for cookie in pickle.load(open(cookies_file, "rb")):

            for i in exlude:
                if i in cookie:
                    del cookie['expiry']

            self.add_cookie(cookie)

    @property
    def wait_for(self):
        return self._wait_for

#-----------------------------------------------------------------------------
