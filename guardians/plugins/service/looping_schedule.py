#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import datetime
import time
import gdapi
import logging

from guardians.plugins.polling_base import PollingBase
from guardians import Config

log = logging.getLogger("guardians")


class ServiceLoopingSchedule(PollingBase):

    def __init__(self, *args, **kwargs):
        super(ServiceLoopingSchedule, self).__init__(*args, **kwargs)
        self.client = gdapi.Client(url=Config.api_url(),
                                   access_key=Config.access_key(),
                                   secret_key=Config.secret_key())
        self.base_param = {'endTime_null': True,
                           'limit': 100,
                           'sort': 'id',
                           'order': 'desc'}

    def perform(self):
        services = self.client.list_processInstance(processName='service.activate',
                                                    exitReason='TIMEOUT',
                                                    **self.base_param)
        self.check_health(services, 'service')
        instances = self.client.list_processInstance(processName='instance.start',
                                                     exitReason='UNKNOWN_EXCEPTION',
                                                     **self.base_param)
        self.check_health(instances, 'instance')

    def check_health(self, processes, resource_type):
        dt = datetime.datetime.utcnow()
        current_ts = int(time.mktime(dt.timetuple())*1000)
        for ps in processes.data:
            timeout = current_ts - ps.startTimeTS
            if resource_type == 'service':
                if timeout > Config.service_timeout():
                    log.info('#####bad service: %s , id: %s####' % (ps.data.name,
                                                                    ps.resourceId))
                    self.remove_service(ps.resourceId)
            if resource_type == 'instance':
                instance = self.client.by_id_instance(ps.resourceId)
                if instance.startCount > Config.instance_start_count():
                    log.info('#####bad instance id: %s####' % (ps.resourceId))
                    self.remove_service_by_instance(instance)

    def remove_service(self, id):
        service = self.client.by_id_service(id)
        if service.state != 'removed':
            try:
                self.client.action(service, 'remove')
                log.info('####remove service: %s####' % id)
            except Exception, e:
                log.error(e)


    def remove_service_by_instance(self, instance):
        for service in instance.services().data:
            try:
                self.client.action(service, 'remove')
                log.info('####remove service: %s####' % instance.id)
            except Exception, e:
                log.error(e)

