#!/usr/bin/env python
#
# Copyright (C) 2017 The Android Open Source Project
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

from webapp.src import vtslab_status
from webapp.src.handlers import base
from webapp.src.scheduler import schedule_worker
from webapp.src.proto import model

from google.appengine.ext import ndb


def test_type_text(test_type, join_str=", "):
    """Generates text to represent in HTML with given test type.

    Args:
        test_type: an integer, test type value.
        join_str: a string, join separator.

    Returns:
        A string of test type.
    """
    text_list = []

    if not test_type:
        return "Unknown"

    if (test_type & 3) == (
            vtslab_status.TEST_TYPE_DICT[vtslab_status.TEST_TYPE_UNKNOWN]):
        return "Unknown"

    if test_type & vtslab_status.TEST_TYPE_DICT[vtslab_status.TEST_TYPE_TOT]:
        text_list.append("ToT")
    if test_type & vtslab_status.TEST_TYPE_DICT[vtslab_status.TEST_TYPE_OTA]:
        text_list.append("OTA")
    if test_type & vtslab_status.TEST_TYPE_DICT[vtslab_status.TEST_TYPE_SIGNED]:
        text_list.append("Signed")

    return join_str.join(text_list)


class JobStats(object):
    """Job stats class.

    Attributes:
        boot_error: int, the number of boot-up error jobs.
        created: int, the number of created jobs.
        completed: int, the number of completed jobs.
        expired: int, the number of expired jobs.
        infra_error: int, the number of infra error jobs.
        running: int, the number of running jobs.
        ready: int, the number of ready jobs.
        unknown: int, the number of unknown jobs.
    """

    boot_error = 0
    created = 0
    completed = 0
    expired = 0
    infra_error = 0
    running = 0
    ready = 0
    unknown = 0


class JobBase(base.BaseHandler):
    """Base class for job pages."""

    def _UpdateStats(self, stats, job):
        """Updates the stats using the state info of a given job.

        Args:
            stats: JobStats, the stats class to update.
            job: JobModel, the job to check.
        """
        stats.created += 1
        if job.status == vtslab_status.JOB_STATUS_DICT["complete"]:
            stats.completed += 1
        elif job.status == vtslab_status.JOB_STATUS_DICT["leased"]:
            stats.running += 1
        elif job.status == vtslab_status.JOB_STATUS_DICT["ready"]:
            stats.ready += 1
        elif job.status == vtslab_status.JOB_STATUS_DICT["infra-err"]:
            stats.infra_error += 1
        elif job.status == vtslab_status.JOB_STATUS_DICT["bootup-err"]:
            stats.boot_error += 1
        elif job.status == vtslab_status.JOB_STATUS_DICT["expired"]:
            stats.expired += 1
        else:
            stats.unknown += 1


class JobPage(JobBase):
    """Main class for /job web page."""

    def get(self):
        """Generates an HTML page based on the job queue info kept in DB."""
        self.template = "job.html"

        job_query = model.JobModel.query()
        jobs = job_query.fetch()

        now = datetime.datetime.now()
        stats_all = JobStats()
        stats_24hrs = JobStats()
        stats_72hrs = JobStats()
        if jobs:
            for job in jobs:
                self._UpdateStats(stats_all, job)
                if now - job.timestamp <= datetime.timedelta(hours=24):
                    self._UpdateStats(stats_24hrs, job)
                if now - job.timestamp <= datetime.timedelta(hours=72):
                    self._UpdateStats(stats_72hrs, job)

        template_values = {
            "jobs": sorted(jobs, key=lambda x: x.timestamp,
                           reverse=True),
            "stats_all": stats_all,
            "stats_24hrs": stats_24hrs,
            "stats_72hrs": stats_72hrs,
            "test_type_text": test_type_text
        }

        self.render(template_values)


class CreateJobTemplatePage(base.BaseHandler):
    """Main class for /create_job_template web page."""

    def get(self):
        """Generates an HTML page to get custom job info."""
        self.template = "create_job_template.html"
        template_values = {}
        self.render(template_values)


class CreateJobPage(JobBase):
    """Main class for /create_job web page."""

    def get(self):
        """Generates an HTML page that stores the provided custom job info to DB."""
        self.template = "job.html"

        serials = self.request.get("serial", default_value="").split(",")

        # TODO: check serial >= shards and select only required ones
        device_query = model.DeviceModel.query(model.DeviceModel.serial.IN(
            serials))
        devices = device_query.fetch()
        error_devices = []
        for device in devices:
            if device.scheduling_status in [
                    vtslab_status.DEVICE_SCHEDULING_STATUS_DICT["reserved"],
                    vtslab_status.DEVICE_SCHEDULING_STATUS_DICT["use"]
            ]:
                error_devices.append(device.serial)

        if error_devices:
            message = "Can't create a job because at some devices " \
                      "are not available (%s)." % error_devices
        else:
            devices_to_put = []
            for device in devices:
                device.scheduling_status = (
                    vtslab_status.DEVICE_SCHEDULING_STATUS_DICT["reserved"])
                devices_to_put.append(device)
            if devices_to_put:
                ndb.put_multi(devices_to_put)

            message = "A new job is created!"

            new_job = model.JobModel()
            new_job.hostname = self.request.get("hostname", default_value="")
            new_job.priority = str(vtslab_status.GetPriorityValue(
                self.request.get("priority", default_value="high")))
            new_job.test_name = self.request.get("test_name", default_value="")
            new_job.device = self.request.get("device", default_value="")
            new_job.period = int(self.request.get("period",
                                                  default_value="high"))
            new_job.serial.extend(serials)

            new_job.manifest_branch = self.request.get("manifest_branch",
                                                       default_value="")
            new_job.build_target = self.request.get("build_target",
                                                    default_value="")

            new_job.shards = int(self.request.get(
                "shards", default_value=str(len(new_job.serial))))
            new_job.param = self.request.get("param",
                                             default_value=[]).split(",")

            new_job.gsi_branch = self.request.get("gsi_branch",
                                                  default_value="")
            new_job.gsi_build_target = self.request.get("gsi_build_target",
                                                        default_value="")
            new_job.gsi_build_id = self.request.get("gsi_build_id",
                                                    default_value="latest")
            new_job.gsi_pab_account_id = self.request.get("gsi_pab_account_id",
                                                          default_value="")

            new_job.test_branch = self.request.get("test_branch",
                                                   default_value="")
            new_job.test_build_target = self.request.get("test_build_target",
                                                         default_value="")
            new_job.test_build_id = self.request.get("test_build_id",
                                                     default_value="latest")
            new_job.test_pab_account_id = self.request.get(
                "test_pab_account_id", default_value="")

            new_job.build_id = self.request.get("build_id",
                                                default_value="latest")
            new_job.pab_account_id = self.request.get("pab_account_id",
                                                      default_value="")
            new_job.status = vtslab_status.JOB_STATUS_DICT["ready"]
            new_job.timestamp = datetime.datetime.now()

            test_type = schedule_worker.GetTestVersionType(
                new_job.manifest_branch, new_job.gsi_branch)
            if new_job.require_signed_device_build:
                test_type |= vtslab_status.TEST_TYPE_DICT[
                    vtslab_status.TEST_TYPE_SIGNED]
            test_type |= (
                vtslab_status.TEST_TYPE_DICT[vtslab_status.TEST_TYPE_MANUAL])
            new_job.test_type = test_type

            new_job.put()

        job_query = model.JobModel.query()
        jobs = job_query.fetch()

        now = datetime.datetime.now()
        stats_all = JobStats()
        stats_24hrs = JobStats()
        stats_72hrs = JobStats()
        if jobs:
            for job in jobs:
                self._UpdateStats(stats_all, job)
                if now - job.timestamp <= datetime.timedelta(hours=24):
                    self._UpdateStats(stats_24hrs, job)
                if now - job.timestamp <= datetime.timedelta(hours=72):
                    self._UpdateStats(stats_72hrs, job)

        template_values = {
            "message": message,
            "jobs": sorted(jobs, key=lambda x: x.timestamp,
                           reverse=True),
            "stats_all": stats_all,
            "stats_24hrs": stats_24hrs,
            "stats_72hrs": stats_72hrs,
            "test_type_text": test_type_text
        }

        self.render(template_values)
