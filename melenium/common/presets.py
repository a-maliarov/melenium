# -*- coding: utf-8 -*-

"""
melenium.presets
~~~~~~~~~~~~~~~~

List of chrome capabilities presets to be used by ChromeCapabilities.

"""

__all__ = ['PRESETS']

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

PRESETS = {
    'empty': EMPTY_CAPABILITIES,
    'maliarov': MALIAROV_BASIC_PRESET
}

#-----------------------------------------------------------------------------
