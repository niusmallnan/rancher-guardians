#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import abc
import time
import sched
import logging

from guardians import Config
from guardians.plugins import PluginBase


log = logging.getLogger("guardians")


class PollingBase(PluginBase):

    def __init__(self, *args, **kwargs):
        super(PollingBase, self).__init__(*args, **kwargs)
        self.scheduler = sched.scheduler(time.time, time.sleep)


    @abc.abstractmethod
    def perform():
        """
        an abstract method need to be implemented
        """
    def run(self):
        log.info('run polling task')
        self.scheduler.enter(Config.polling_duration(), 100, self.run, ())
        self.perform()
        self.scheduler.run()

    def exit(self):
        pass
