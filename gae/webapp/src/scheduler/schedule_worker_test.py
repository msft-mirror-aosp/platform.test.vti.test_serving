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
from webapp.src.testing import unittest_base


class ScheduleHandlerTest(unittest_base.UnitTestBase):
    """Tests for ScheduleHandler.

    Attributes:
        scheduler: A mock schedule_worker.ScheduleHandler.
    """

    def setUp(self):
        """Initializes test"""
        super(ScheduleHandlerTest, self).setUp()
        # Mocking ScheduleHandler and essential methods.
        self.scheduler = schedule_worker.ScheduleHandler(mock.Mock())
        self.scheduler.response = mock.Mock()
        self.scheduler.response.write = mock.Mock()
        self.scheduler.request.get = mock.MagicMock(return_value="")

    def testSimpleJobCreation(self):
        """Asserts a job is created.

        This test defines that each model only has a single entity, and asserts
        that a job is created.
        """
        lab = self.GenerateLabModel()
        lab.put()

        device = self.GenerateDeviceModel(hostname=lab.hostname)
        device.put()

        schedule = self.GenerateScheduleModel(
            device_model=device, lab_model=lab)
        schedule.put()

        build_dict = self.GenerateBuildModel(schedule)
        for key in build_dict:
            build_dict[key].put()

        self.scheduler.post()
        self.assertEqual(1, len(model.JobModel.query().fetch()))
        print("A job is created successfully.")

        device_query = model.DeviceModel.query(
            model.DeviceModel.serial == device.serial)
        device = device_query.fetch()[0]
        self.assertEqual(Status.DEVICE_SCHEDULING_STATUS_DICT["reserved"],
                         device.scheduling_status)
        print("A device is reserved successfully.")


if __name__ == "__main__":
    unittest.main()
