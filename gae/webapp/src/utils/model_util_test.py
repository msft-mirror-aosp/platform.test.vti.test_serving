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
from webapp.src.scheduler import schedule_worker
from webapp.src.utils import model_util

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class ModelTest(unittest.TestCase):
    """Tests for PeriodicJobHeartBeat cron class.

    Attributes:
        testbed: A Testbed instance which provides local unit testing.
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
        # import job_heartbeat after setting app_id.

    def tearDown(self):
        self.testbed.deactivate()

    def testJobAndScheduleModel(self):
        """Asserts JobModel and ScheduleModel.

        When JobModel's status is changed, ScheduleModel's error_count is
        changed based on the status. This should not be applied before JobModel
        entity is updated to Datastore.
        """
        # schedule information
        priority = "top"
        period = 360
        build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        manifest_branch = "manifest_branch"
        build_target = "device_build_target-user"
        pab_account_id = "1234567890"
        shards = 1
        retry_count = 1
        gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        gsi_branch = "gsi_branch"
        gsi_build_target = "gsi_build_target-user"
        gsi_pab_account_id = "1234567890"
        test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        test_branch = "test_branch"
        test_build_target = "test_build_target-user"
        test_pab_account_id = "1234567890"

        lab_name = "test_lab"
        host_name = "test_host"
        device_name = "device"

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
        build.manifest_branch = test_branch
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

        # create a device
        device = model.DeviceModel()
        device.hostname = host_name
        device.product = device_name
        device.serial = "serial"
        device.status = Status.DEVICE_STATUS_DICT["fastboot"]
        device.scheduling_status = (
            Status.DEVICE_SCHEDULING_STATUS_DICT["free"])
        device.timestamp = datetime.datetime.now()
        device.put()

        # create a schedule
        schedule = model.ScheduleModel()
        schedule.priority = priority
        schedule.test_name = "test/{}".format(device_name)
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
        schedule.device.append("{}/{}".format(lab_name, device_name))
        schedule.put()

        schedule = model.ScheduleModel.query().fetch()[0]
        schedule.put()

        # Mocking ScheduleHandler and essential methods.
        scheduler = schedule_worker.ScheduleHandler(mock.Mock())
        scheduler.response = mock.Mock()
        scheduler.response.write = mock.Mock()

        print("\nCreating a job...")
        scheduler.post()
        jobs = model.JobModel.query().fetch()
        self.assertEqual(1, len(jobs))

        print("Occurring infra error...")
        job = jobs[0]
        job.status = Status.JOB_STATUS_DICT["infra-err"]
        parent_schedule = job.parent_schedule.get()
        parent_from_db = model.ScheduleModel.query().fetch()[0]

        # in test error_count could be None but in real there will be no None.
        self.assertNotEqual(1, parent_schedule.error_count)
        self.assertNotEqual(1, parent_from_db.error_count)

        # error count should be changed after put
        job.put()
        model_util.UpdateParentSchedule(job, job.status)
        self.assertEqual(1, parent_schedule.error_count)
        self.assertEqual(1, parent_from_db.error_count)

        print("Suspending a job...")
        for num in xrange(2):
            jobs = model.JobModel.query().fetch()
            for job in jobs:
                job.timestamp = datetime.datetime.now() - datetime.timedelta(
                    minutes=(period + 10))
                job.put()

            parent_from_db = model.ScheduleModel.query().fetch()[0]
            self.assertEqual(1 + num, parent_schedule.error_count)
            self.assertEqual(1 + num, parent_from_db.error_count)

            # reset a device manually to re-schedule
            device = model.DeviceModel.query().fetch()[0]
            device.status = Status.DEVICE_STATUS_DICT["fastboot"]
            device.scheduling_status = (
                Status.DEVICE_SCHEDULING_STATUS_DICT["free"])
            device.timestamp = datetime.datetime.now()
            device.put()

            scheduler.post()
            jobs = model.JobModel.query().fetch()
            self.assertEqual(2 + num, len(jobs))

            ready_jobs = model.JobModel.query(
                model.JobModel.status == Status.JOB_STATUS_DICT[
                    "ready"]).fetch()
            self.assertEqual(1, len(ready_jobs))

            ready_job = ready_jobs[0]
            ready_job.status = Status.JOB_STATUS_DICT["infra-err"]
            parent_schedule = ready_job.parent_schedule.get()
            parent_from_db = model.ScheduleModel.query().fetch()[0]
            self.assertEqual(1 + num, parent_schedule.error_count)
            self.assertEqual(1 + num, parent_from_db.error_count)

            # # error count should be changed after put
            ready_job.put()
            model_util.UpdateParentSchedule(ready_job, ready_job.status)
            self.assertEqual(2 + num, parent_schedule.error_count)
            self.assertEqual(2 + num, parent_from_db.error_count)

        print("Asserting a schedule's suspend status...")
        # after three errors the schedule should be suspended.
        schedule_from_db = model.ScheduleModel.query().fetch()[0]
        schedule_from_db.put()
        self.assertEqual(3, schedule_from_db.error_count)
        self.assertEqual(True, schedule_from_db.suspended)

        # reset a device manually to re-schedule
        device = model.DeviceModel.query().fetch()[0]
        device.status = Status.DEVICE_STATUS_DICT["fastboot"]
        device.scheduling_status = (
            Status.DEVICE_SCHEDULING_STATUS_DICT["free"])
        device.timestamp = datetime.datetime.now()
        device.put()

        print("Asserting that job creation is blocked...")
        jobs = model.JobModel.query().fetch()
        self.assertEquals(3, len(jobs))

        for job in jobs:
            job.timestamp = datetime.datetime.now() - datetime.timedelta(
                minutes=(period + 10))
            job.put()

        scheduler.post()

        # a job should not be created.
        jobs = model.JobModel.query().fetch()
        self.assertEquals(3, len(jobs))

        print("Asserting that job creation is allowed after resuming...")
        schedule_from_db = model.ScheduleModel.query().fetch()[0]
        schedule_from_db.suspended = False
        schedule_from_db.put()

        scheduler.post()

        jobs = model.JobModel.query().fetch()
        self.assertEquals(4, len(jobs))


if __name__ == "__main__":
    unittest.main()
