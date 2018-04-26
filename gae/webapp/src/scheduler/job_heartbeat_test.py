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
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from webapp.src import vtslab_status as Status
from webapp.src.proto import model
from webapp.src.scheduler import job_heartbeat
from webapp.src.scheduler import schedule_worker

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class JobHeartbeatTest(unittest.TestCase):
    """Tests for PeriodicJobHeartBeat cron class.

    Attributes:
        testbed: A Testbed instance which provides local unit testing.
        job_heartbeat: A mock job_heartbeat.PeriodicJobHeartBeat instance.
    """

    def setUp(self):
        """Initializes test"""
        # Create the Testbed class instance and initialize service stubs.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id="vtslab-schedule-unittest")
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_mail_stub()
        # Clear cache between tests.
        ndb.get_context().clear_cache()
        # Mocking PeriodicJobHeartBeat and essential methods.
        self.job_heartbeat = job_heartbeat.PeriodicJobHeartBeat(mock.Mock())
        self.job_heartbeat.response = mock.Mock()
        self.job_heartbeat.response.write = mock.Mock()

    def tearDown(self):
        self.testbed.deactivate()

    def testJobHearbeat(self):
        """"""
        # schedule information
        priority = "top"
        period = 360
        build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        manifest_branch = "manifest_branch"
        build_target = "device_build_target-user"
        pab_account_id = "1234567890"
        shards = 2
        retry_count = 1
        gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        gsi_branch = "gsi_branch"
        gsi_build_target = "gsi_build_target-user"
        gsi_pab_account_id = "1234567890"
        test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        test_branch = "gsi_branch"
        test_build_target = "gsi_build_target-user"
        test_pab_account_id = "1234567890"

        lab_name = "test_lab"
        host_name = "test_host"
        devices_list = ["device1", "device2"]

        # create a device build
        build = model.BuildModel()
        build.manifest_branch = manifest_branch
        build.build_id = "1000000"
        build.build_target = "device_build_target"
        build.build_type = "user"
        build.artifact_type = "device"
        build.timestamp = datetime.datetime.now()
        build.signed = False
        build.put()

        # create a gsi build
        build = model.BuildModel()
        build.manifest_branch = gsi_branch
        build.build_id = "2000000"
        build.build_target = "gsi_build_target"
        build.build_type = "user"
        build.artifact_type = "gsi"
        build.timestamp = datetime.datetime.now()
        build.signed = False
        build.put()

        # create a test build
        build = model.BuildModel()
        build.manifest_branch = gsi_branch
        build.build_id = "3000000"
        build.build_target = "test_build_target"
        build.build_type = "user"
        build.artifact_type = "test"
        build.timestamp = datetime.datetime.now()
        build.signed = False
        build.put()

        # create a lab
        lab = model.LabModel()
        lab.name = lab_name
        lab.hostname = host_name
        lab.owner = "test@google.com"
        lab.put()

        # create devices
        for dev in devices_list:
            for num in xrange(shards):
                device = model.DeviceModel()
                device.hostname = host_name
                device.product = dev
                device.serial = "{}{}".format(dev, num)
                device.status = Status.DEVICE_STATUS_DICT["fastboot"]
                device.scheduling_status = (
                    Status.DEVICE_SCHEDULING_STATUS_DICT["free"])
                device.timestamp = datetime.datetime.now()
                device.put()

        # create schedules
        for device in devices_list:
            schedule = model.ScheduleModel()
            schedule.priority = priority
            schedule.test_name = "test/{}".format(device)
            schedule.period = period
            schedule.build_storage_type = build_storage_type
            schedule.manifest_branch = manifest_branch
            schedule.build_target = build_target
            schedule.device_pab_account_id = pab_account_id
            schedule.shards = shards
            schedule.retry_count = retry_count
            schedule.gsi_storage_type = gsi_storage_type
            schedule.gsi_branch = gsi_branch
            schedule.gsi_build_target = gsi_build_target
            schedule.gsi_pab_account_id = gsi_pab_account_id
            schedule.test_storage_type = test_storage_type
            schedule.test_branch = test_branch
            schedule.test_build_target = test_build_target
            schedule.test_pab_account_id = test_pab_account_id
            schedule.device = []
            schedule.device.append("{}/{}".format(lab_name, device))
            schedule.put()

        # Mocking ScheduleHandler and essential methods.
        scheduler = schedule_worker.ScheduleHandler(mock.Mock())
        scheduler.response = mock.Mock()
        scheduler.response.write = mock.Mock()

        print("Creating jobs...")
        scheduler.post()
        jobs = model.JobModel.query().fetch()
        self.assertEqual(2, len(jobs))

        print("Making jobs get old and running heartbeat monitor...")
        for job in jobs:
            job.status = Status.JOB_STATUS_DICT["leased"]
            job.timestamp = (
                datetime.datetime.now() - datetime.timedelta(minutes=10))
            job.heartbeat_stamp = (
                datetime.datetime.now() - datetime.timedelta(minutes=7))
            job.put()

        self.job_heartbeat.get()

        jobs = model.JobModel.query().fetch()
        for job in jobs:
            self.assertEquals(Status.JOB_STATUS_DICT["infra-err"], job.status)

        devices = model.DeviceModel.query().fetch()
        for device in devices:
            self.assertEquals(Status.DEVICE_SCHEDULING_STATUS_DICT["free"],
                              device.scheduling_status)


if __name__ == "__main__":
    unittest.main()
