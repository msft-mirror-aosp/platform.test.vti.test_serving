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

    def testPriorityScheduling(self):
        """Asserts job creation with priority scheduling."""
        product = "product"
        high_priority_schedule_test_name = "high_test"
        medium_priority_schedule_test_name = "medium_test"

        lab = self.GenerateLabModel()
        lab.put()

        device = self.GenerateDeviceModel(
            hostname=lab.hostname, product=product)
        device.put()

        schedule_high = self.GenerateScheduleModel(
            device_model=device,
            lab_model=lab,
            priority="high",
            test_name=high_priority_schedule_test_name)
        schedule_high.put()

        schedule_medium = self.GenerateScheduleModel(
            device_model=device,
            lab_model=lab,
            priority="medium",
            test_name=medium_priority_schedule_test_name)
        schedule_medium.put()

        build_dict = self.GenerateBuildModel(schedule_high)
        for key in build_dict:
            build_dict[key].put()

        self.scheduler.post()
        schedules = model.ScheduleModel.query().fetch()
        self.assertEqual(schedules[0].test_name,
                         high_priority_schedule_test_name)

    def testPrioritySchedulingWithAging(self):
        """Asserts job creation with priority scheduling with aging."""
        product = "product"
        high_priority_schedule_test_name = "high_test"
        medium_priority_schedule_test_name = "medium_test"
        schedule_period_minute = 100

        lab = self.GenerateLabModel()
        lab.put()

        device = self.GenerateDeviceModel(
            hostname=lab.hostname, product=product)
        device.put()

        schedules = []
        schedule_high = self.GenerateScheduleModel(
            device_model=device,
            lab_model=lab,
            test_name=high_priority_schedule_test_name,
            period=schedule_period_minute,
            priority="high")
        schedule_high.put()
        schedules.append(schedule_high)

        schedule_medium = self.GenerateScheduleModel(
            device_model=device,
            lab_model=lab,
            test_name=medium_priority_schedule_test_name,
            period=schedule_period_minute,
            priority="medium")
        schedule_medium.put()
        schedules.append(schedule_medium)

        for schedule in schedules:
            build_dict = self.GenerateBuildModel(schedule)
            for key in build_dict:
                build_dict[key].put()

        high_original_priority_value = schedule_high.priority_value
        medium_original_priority_value = schedule_medium.priority_value

        # On first attempt, "high" priority will create a job.
        self.scheduler.post()
        jobs = model.JobModel.query().fetch()
        self.assertEqual(jobs[0].test_name, high_priority_schedule_test_name)

        # medium priority schedule's priority value will be decreased.
        self.assertEqual(medium_original_priority_value - 1,
                         schedule_medium.priority_value)

        self.PassTime(minutes=schedule_period_minute + 1)
        self.ResetDevices()

        # On second attempt, "high" priority will create a job.
        self.scheduler.post()
        jobs = model.JobModel.query().fetch()
        jobs.sort(key=lambda x: x.timestamp, reverse=True)  # latest first
        self.assertEqual(jobs[0].test_name, high_priority_schedule_test_name)

        # medium priority schedule's priority value will be decreased again.
        self.assertEqual(medium_original_priority_value - 2,
                         schedule_medium.priority_value)

        while schedule_medium.priority_value >= high_original_priority_value:
            self.PassTime(minutes=schedule_period_minute + 1)
            self.ResetDevices()
            self.scheduler.post()

        # at last, medium priority schedule should be able to create a job.
        self.PassTime(minutes=schedule_period_minute + 1)
        self.ResetDevices()
        self.scheduler.post()

        jobs = model.JobModel.query().fetch()
        jobs.sort(key=lambda x: x.timestamp, reverse=True)  # latest first
        self.assertEqual(jobs[0].test_name, medium_priority_schedule_test_name)

        # after a job is created, its priority value should be restored.
        self.assertEqual(schedule_medium.priority_value,
                         medium_original_priority_value)

    def testPrioritySchedulingWithAgingForMultiDevices(self):
        """Asserts job creation with priority scheduling for multi devices."""
        product1 = "product1"
        product2 = "product2"
        schedule_period_minute = 360

        lab = self.GenerateLabModel()
        lab.put()

        device1 = self.GenerateDeviceModel(
            hostname=lab.hostname, product=product1)
        device1.put()

        device2 = self.GenerateDeviceModel(
            hostname=lab.hostname, product=product2)
        device2.put()

        schedule1_l = self.GenerateScheduleModel(
            device_model=device1,
            lab_model=lab,
            priority="low",
            period=schedule_period_minute)
        schedule1_l.put()

        schedule1_h = self.GenerateScheduleModel(
            device_model=device1,
            lab_model=lab,
            priority="high",
            period=schedule_period_minute)
        schedule1_h.put()

        schedule2_m = self.GenerateScheduleModel(
            device_model=device2,
            lab_model=lab,
            priority="medium",
            period=schedule_period_minute)
        schedule2_m.put()

        schedule2_h = self.GenerateScheduleModel(
            device_model=device2,
            lab_model=lab,
            priority="high",
            period=schedule_period_minute)
        schedule2_h.put()

        schedule1_l_original_priority_value = schedule1_l.priority_value
        schedule2_m_original_priority_value = schedule2_m.priority_value

        for schedule in [schedule2_m, schedule2_h]:
            build_dict = self.GenerateBuildModel(schedule)
            for key in build_dict:
                build_dict[key].put()

        # create jobs
        self.scheduler.post()

        # schedule2_m will not get a change to create a job.
        jobs = model.JobModel.query().fetch()
        self.assertTrue(
            any([job.test_name == schedule2_h.test_name for job in jobs]))
        self.assertFalse(
            any([job.test_name == schedule2_m.test_name for job in jobs]))

        # schedule2_m's priority value should be decreased.
        self.assertTrue(schedule2_m_original_priority_value - 1,
                        schedule2_m.priority_value)

        # schedule1_l's priority value should not be changed because all other
        # schedules for device1 were also failed to created a job.
        self.assertTrue(schedule1_l_original_priority_value,
                        schedule1_l.priority_value)

        for num in range(3):
            self.assertTrue(schedule2_m_original_priority_value - 1 - num,
                            schedule2_m.priority_value)
            self.PassTime(minutes=schedule_period_minute + 1)
            self.ResetDevices()
            self.scheduler.post()
            self.assertFalse(
                any([job.test_name == schedule2_m.test_name for job in jobs]))
            self.assertTrue(schedule1_l_original_priority_value,
                            schedule1_l.priority_value)

        # device1 is ready for scheduling.
        for schedule in [schedule1_l, schedule1_h]:
            build_dict = self.GenerateBuildModel(schedule)
            for key in build_dict:
                build_dict[key].put()

        # after 4 times of failure, now schedule2_m can create a job.
        self.PassTime(minutes=schedule_period_minute + 1)
        self.ResetDevices()
        self.scheduler.post()

        jobs = model.JobModel.query().fetch()
        self.assertTrue(
            any([job.test_name == schedule2_m.test_name for job in jobs]))

        # now schedule_1's priority value should be changed.
        self.assertEquals(schedule1_l_original_priority_value - 1,
                          schedule1_l.priority_value)


if __name__ == "__main__":
    unittest.main()
