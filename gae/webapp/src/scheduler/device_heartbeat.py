#!/usr/bin/env python
#
# Copyright (C) 2018 The Android Open Source Project
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

import datetime
import webapp2

from webapp.src import vtslab_status as Status
from webapp.src.proto import model
from webapp.src.utils import logger

DEVICE_RESPONSE_TIMEOUT_SECONDS = 300


class PeriodicDeviceHeartBeat(webapp2.RequestHandler):
    """Main class for /tasks/device_heartbeat.

    Used to find lost devices and change their status properly.

    Attributes:
        logger: Logger class
    """

    def __init__(self):
        self.logger = logger.Logger()

    def get(self):
        """Generates an HTML page based on the task schedules kept in DB."""
        self.logger.LogClear()

        device_query = model.DeviceModel.query()
        devices = device_query.fetch()
        lost_devices = [
            x for x in devices
            if (datetime.datetime.now() - x.timestamp
                ).seconds >= DEVICE_RESPONSE_TIMEOUT_SECONDS
               and x.status != Status.DEVICE_STATUS_DICT["no-response"]
        ]
        for device in lost_devices:
            self.logger.LogPrintln("Device[{}] is not responding.".format(
                device.serial))
            device.status = Status.DEVICE_STATUS_DICT["no-response"]
            device.put()

        self.response.write(
            "<pre>\n" + "\n".join(self.logger.Get()) + "\n</pre>")
