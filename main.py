#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import logging
import argparse
import sys

from guardians import Config, plugins


log = logging.getLogger("guardians")


def _arg():
    parser = argparse.ArgumentParser(add_help=help)

    parser.add_argument('--url', default=Config.api_url())
    parser.add_argument('--access-key', default=Config.access_key())
    parser.add_argument('--secret-key', default=Config.secret_key())
    parser.add_argument('--polling-duration', type=int,
                        default=Config.polling_duration())
    parser.add_argument('--service-timeout', type=int,
                        default=Config.service_timeout())
    parser.add_argument('--instance-start-count', type=int,
                        default=Config.instance_start_count())

    return parser.parse_args()


def main():
    format = '%(asctime)s %(levelname)s %(name)s [%(thread)s] ' \
             '[%(filename)s:%(lineno)s] %(message)s '
    logging.basicConfig(level=logging.INFO, format=format)
    args = _arg()

    Config.set_api_url(args.url)
    Config.set_access_key(args.access_key)
    Config.set_secret_key(args.secret_key)

    for cls in plugins.get_task_classes():
        cls().run()
    sys.exit(0)


if __name__=='__main__':
    main()
