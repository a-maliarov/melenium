# -*- coding: utf-8 -*-

"""
melenium.wait_for
~~~~~~~~~~~~~~~~~

"""

__all__ = ['WaitFor']

import time

try:
    from bs4 import BeautifulSoup as BS
except ImportError:
    from beautifulsoup4 import BeautifulSoup as BS

#-----------------------------------------------------------------------------

class WaitFor(object):

    def __init__(self, driver):
        self._driver = driver

    def phrase_in_link(self, timeout, phrase='/'):
        counter = 0

        while phrase not in self._driver.current_url:
            time.sleep(1)
            counter += 1

            if counter == timeout:
                return None

    def element_in_dom(self, timeout, *argv, **kwargs):
        counter = 0

        while BS(self._driver.page_source, features = 'html.parser').find(*argv, **kwargs) == None:
            time.sleep(1)
            counter += 1

            if counter == timeout:
                return None

#-----------------------------------------------------------------------------
