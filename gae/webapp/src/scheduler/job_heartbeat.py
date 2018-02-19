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

JOB_RESPONSE_TIMEOUT_SECONDS = 300


class PeriodicJobHeartBeat(webapp2.RequestHandler):
    """Main class for /tasks/job_heartbeat.

    Used to find lost jobs and change their status properly.

    Attributes:
        logger: Logger class
    """

    def __init__(self):
        self.logger = logger.Logger()

    def get(self):
        """Generates an HTML page based on the task schedules kept in DB."""
        self.logger.LogClear()

        job_query = model.JobModel.query()
        jobs = job_query.fetch()

        lost_jobs = [
            x for x in jobs
            if x.heartbeat_stamp and
            (datetime.datetime.now() - x.heartbeat_stamp
             ).seconds >= JOB_RESPONSE_TIMEOUT_SECONDS
            and x.status == Status.JOB_STATUS_DICT["leased"]
        ]
        for job in lost_jobs:
            self.logger.LogPrintln("Lost job found")
            self.logger.LogPrintln(
                "[hostname]{} [device]{} [testname]{}".format(
                    job.hostname, job.device, job.testname))
            job.status = Status.JOB_STATUS_DICT["infra-err"]
            job.put()

            device_query = model.DeviceModel.query()
            devices = device_query.fetch()

            devices_in_job = [x for x in devices if x.serial in job.serial]

            for device in devices_in_job:
                if job.status == Status.JOB_STATUS_DICT["leased"]:
                    status = Status.DEVICE_SCHEDULING_STATUS_DICT["use"]
                elif job.status == Status.JOB_STATUS_DICT["ready"]:
                    status = Status.DEVICE_SCHEDULING_STATUS_DICT["reserved"]
                else:
                    status = Status.DEVICE_SCHEDULING_STATUS_DICT["free"]
                device.scheduling_status = status
                device.put()

        self.response.write(
            "<pre>\n" + "\n".join(self.logger.Get()) + "\n</pre>")
