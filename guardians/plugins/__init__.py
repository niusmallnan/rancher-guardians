#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import abc
import logging
import os
import imp
import sys
import six
import inspect


log = logging.getLogger("guardians")


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):

    @abc.abstractmethod
    def run():
        """
        an abstract method need to be implemented
        """


def _load(module, plugin_path):
    std_name = "guardians.plugins.%s" % module
    if std_name in sys.modules:
        return

    log.info("Loading Plugin: %s from %s", module, plugin_path)
    try:
        m = imp.find_module(module, [plugin_path])
        return imp.load_module(std_name, m[0], m[1], m[2])
    except Exception:
        log.exception('Exception loading module')


def _init(full_path):
    modules = []

    for d in os.listdir(full_path):
        plugin_path = os.path.join(full_path, d)
        if os.path.exists(os.path.join(plugin_path, "__init__.py")):
            modules.append(_load(d, full_path))

    return modules


def get_task_classes():
    classes = []
    for m in _init(os.path.dirname(os.path.abspath(__file__))):
        for name, obj in inspect.getmembers(m, inspect.isclass):
            if issubclass(obj, PluginBase):
                classes.append(obj)

    return classes

