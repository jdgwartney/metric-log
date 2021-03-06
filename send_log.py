#!/usr/bin/env python
#
# Copyright 2016 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from datetime import datetime
from tspapi import API
from tspapi import Measurement
from random import randrange
from logme import LogMe
from time import sleep
import logging


class SendLog(object):
    def __init__(self):
        """
        Initialize our example class to show how to log measurements
        """
        self.api = API()
        self.logme = LogMe(db_path='send_log.db')
        logging.basicConfig(level=logging.INFO)

    def send_measurements(self):
        """
        Continuously loops sending measurements using the python api and logs the values collected.
        :return:
        """
        while True:
            timestamp = int(datetime.now().strftime("%s"))
            m = Measurement(metric='CPU', value=randrange(0, 100) / 100.0, source='foo', timestamp=timestamp)
            self.api.measurement_create(metric=m.metric, source=m.source, value=m.value, timestamp=m.timestamp)
            self.logme.log(metric=m.metric, value=m.value, source=m.source, timestamp=m.timestamp)

            measurements = []
            measurements.append(Measurement(metric='CPU', value=randrange(0, 100) / 100.0,
                                            source='red', timestamp=timestamp))
            measurements.append(Measurement(metric='CPU', value=randrange(0, 100) / 100.0,
                                            source='green', timestamp=timestamp))
            measurements.append(Measurement(metric='CPU', value=randrange(0, 100) / 100.0,
                                            source='blue', timestamp=timestamp))
            self.api.measurement_create_batch(measurements)
            self.logme.log_batch(measurements)
            sleep(5)


def execute():
    """
    Create an instance of SendLog and call its method to generate measurements using the Pulse API and
    use the LogMe instance to log measurements sent to Pulse
    :return:
    """
    s = SendLog()
    s.send_measurements()


if __name__ == '__main__':
    execute()
