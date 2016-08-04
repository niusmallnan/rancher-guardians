from __future__ import unicode_literals, print_function

import argparse
import os
import threading
import datetime
import time
import gdapi

args = None
client = None

#GDAPI_URL = 'http://192.168.252.79:8080/v1'
#GDAPI_ACCESS_KEY = '72896B1B4175537ACF73'
#GDAPI_SECRET_KEY= 'vqw9mG8BuPVMJFFwhbVQRfXWirmht8LCsrRyPWAF'

#DEFAULT_TIMEOUT = 60 * 10 * 1000 #millisecond


def env(vars, **kwargs):
    value = os.environ.get(vars)
    if value:
        return value
    return kwargs.get('default', '')


def register_args():
    """TODO: Docstring for register_args.
    :returns: TODO

    """
    global args
    arg_cattle_url = env('CATTLE_URL')
    arg_cattle_acckey = env('CATTLE_ACCESS_KEY')
    arg_cattle_seckey = env('CATTLE_SECRET_KEY')
    arg_timer = env('TIMER', default=60) #seconds
    arg_service_timeout = env('SERVICE_TIMEOUT', default=60*1000*10)
    arg_instance_start_count = env('INSTANCE_START_COUNT', default=5)

    parser = argparse.ArgumentParser(add_help=help)
    parser.add_argument('--cattle-url', dest='cattle_url',
                        default=arg_cattle_url)
    parser.add_argument('--cattle-access-key', dest='cattle_access_key',
                        default=arg_cattle_acckey)
    parser.add_argument('--cattle-secret-key', dest='cattle_secret_key',
                        default=arg_cattle_seckey)
    parser.add_argument('--timer', dest='timer', type=int, default=arg_timer)
    parser.add_argument('--service-timeout', dest='service_timeout', type=int,
                        default=arg_service_timeout)
    parser.add_argument('--instance-start-count', dest='instance_start_count',
                        type=int, default=arg_instance_start_count)
    args = parser.parse_args()


def remove_service(id):
    service = client.by_id_service(id)
    if service.state != 'removed':
        try:
            client.action(service, 'remove')
            print('####remove service: %s####' % id)
        except Exception, e:
            print(e)


def remove_service_by_instance(instance):
    for service in instance.services().data:
        try:
            client.action(service, 'remove')
            print('####remove service: %s####' % instance.id)
        except Exception, e:
            print(e)


def check_health(processes, resource_type):
    dt = datetime.datetime.utcnow()
    current_ts = int(time.mktime(dt.timetuple())*1000)
    print(processes.data)
    for ps in processes.data:
        timeout = current_ts - ps.startTimeTS
        if resource_type == 'service':
            if timeout > args.service_timeout:
                print('#####bad service: %s , id: %s####' % (ps.data.name,
                                                             ps.resourceId))
                remove_service(ps.resourceId)
        if resource_type == 'instance':
                instance = client.by_id_instance(ps.resourceId)
                if instance.startCount > args.instance_start_count:
                    print('#####bad instance id: %s####' % (ps.resourceId))
                    remove_service_by_instance(instance)


def launch():
    global client
    if not client:
        client = gdapi.Client(url=args.cattle_url,
                              access_key=args.cattle_access_key,
                              secret_key=args.cattle_secret_key)
    running_services = client.list_processInstance(endTime_null=True,
                                                   limit=100,
                                                   sort=id,
                                                   order='desc',
                                                   processName='service.activate',
                                                   exitReason='TIMEOUT')
    check_health(running_services, 'service')

    running_instances = client.list_processInstance(endTime_null=True,
                                                    limit=100,
                                                    sort=id,
                                                    order='desc',
                                                    processName='instance.start',
                                                    exitReason='UNKNOWN_EXCEPTION')
    check_health(running_instances, 'instance')

    threading.Timer(args.timer, launch).start()

if __name__ == '__main__':
    register_args()
    launch()
