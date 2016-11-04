#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os


CONFIG_OVERRIDE = {}


def default_value(name, default):
    if name in CONFIG_OVERRIDE:
        return CONFIG_OVERRIDE[name]
    result = os.environ.get('JUSTEP_%s' % name, default)
    if result == '':
        return default
    return result


class Config:

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def setup_logger():
        return default_value('LOGGER', 'true') == 'true'

    @staticmethod
    def access_key():
        return default_value('ACCESS_KEY', 'admin')

    @staticmethod
    def secret_key():
        return default_value('SECRET_KEY', 'adminpass')

    @staticmethod
    def api_url():
        return default_value('URL', None)

    @staticmethod
    def service_timeout():
        return int(default_value('SERVICE_TIMEOUT', 60))

    @staticmethod
    def instance_start_count():
        return int(default_value('INST_START_COUNT', 15))

    @staticmethod
    def polling_duration():
        return int(default_value('POLLING_DURATION', 20))

    @staticmethod
    def set_api_url(value):
        CONFIG_OVERRIDE['URL'] = value

    @staticmethod
    def set_access_key(value):
        CONFIG_OVERRIDE['ACCESS_KEY'] = value

    @staticmethod
    def set_secret_key(value):
        CONFIG_OVERRIDE['SECRET_KEY'] = value
