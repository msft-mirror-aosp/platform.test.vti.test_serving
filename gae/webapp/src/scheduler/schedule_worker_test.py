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

import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from webapp.src import vtslab_status as Status
from webapp.src.proto import model
from webapp.src.scheduler import schedule_worker

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class ScheduleHandlerTest(unittest.TestCase):
    """Tests for ScheduleHandler.

    Attributes:
        testbed: A Testbed instance which provides local unit testing.
        scheduler: A mock schedule_worker.ScheduleHandler.
    """

    def setUp(self):
        """Initializes test"""
        # Create the Testbed class instance and initialize service stubs.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear cache between tests.
        ndb.get_context().clear_cache()
        # Mocking ScheduleHandler and essential methods.
        self.scheduler = schedule_worker.ScheduleHandler(mock.Mock())
        self.scheduler.response = mock.Mock()
        self.scheduler.response.write = mock.Mock()

    def tearDown(self):
        self.testbed.deactivate()

    def testSimpleJobCreation(self):
        """Asserts a job is created.

        This test defines that each model only has a single entity, and asserts
        that a job is created.
        """
        schedule = model.ScheduleModel()
        schedule.schedule_type = "test"
        schedule.test_name = "vts/vts"
        schedule.manifest_branch = "branch1"
        schedule.build_target = "product1-type1"
        schedule.device = ["test_lab1/product1"]
        schedule.shards = 1
        schedule.build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        schedule.gsi_branch = "gsi_branch"
        schedule.gsi_build_target = "gsi_build_target"
        schedule.test_branch = "test_branch"
        schedule.test_build_target = "test_build_target"
        schedule.require_signed_device_build = False
        schedule.put()

        lab = model.LabModel()
        lab.name = "test_lab1"
        lab.hostname = "test_lab1_host1"
        lab.owner = "test@google.com"
        lab.put()

        device = model.DeviceModel()
        device.status = Status.DEVICE_STATUS_DICT["fastboot"]
        device.scheduling_status = Status.DEVICE_SCHEDULING_STATUS_DICT["free"]
        device.product = "product1"
        device.serial = "serial1"
        device.hostname = "test_lab1_host1"
        device.put()

        build = model.BuildModel()
        build.manifest_branch = "branch1"
        build.build_id = "0000000"
        build.build_target = "product1"
        build.build_type = "type1"
        build.put()

        self.scheduler.post()
        self.assertEqual(1, len(model.JobModel.query().fetch()))
        print("A job is created successfully.")

        device_query = model.DeviceModel.query(
            model.DeviceModel.serial == "serial1")
        device = device_query.fetch()[0]
        self.assertEqual(Status.DEVICE_SCHEDULING_STATUS_DICT["reserved"],
                         device.scheduling_status)
        print("A device is reserved successfully.")


if __name__ == "__main__":
    unittest.main()
