# -*- coding: utf-8 -*-

"""
melenium.capabilities
~~~~~~~~~~~~~~~~~~~~~

Contains ChromeCapabilities.

"""

__all__ = ['ChromeCapabilities']

import base64

from .presets import PRESETS

#-----------------------------------------------------------------------------

class ChromeCapabilities(object):

    def __init__(self, preset='empty'):
        if isinstance(preset, str):
            self.desired = PRESETS[preset].copy()
        elif isinstance(preset, dict):
            self.desired = preset.copy()

    def add_argument(self, argument):
        self.desired['goog:chromeOptions']['args'].append(argument)

    def add_experimental_option(self, experimental_option):
        self.desired['goog:chromeOptions']['prefs'] = experimental_option

    def add_extension(self, extension):
        file_ = open(extension, 'rb')
        encoded_extension = base64.b64encode(file_.read()).decode('UTF-8')
        file_.close()

        self.desired['goog:chromeOptions']['extensions'].append(encoded_extension)

    def set_user_agent(self, user_agent):
        self.add_argument('user-agent={}'.format(user_agent))

    def set_proxy(self, proxy):
        proxy_types = ['httpProxy', 'ftpProxy', 'sslProxy']

        for type in proxy_types:
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
