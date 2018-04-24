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
from webapp.src.tasks import indexing

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class IndexingHandlerTest(unittest.TestCase):
    """Tests for IndexingHandler.

    Attributes:
        testbed: A Testbed instance which provides local unit testing.
        indexing_handler: A mock IndexingHandler instance.
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
        # Mocking IndexingHandler.
        self.indexing_handler = indexing.IndexingHandler(mock.Mock())
        self.indexing_handler.request = mock.Mock()

    def tearDown(self):
        self.testbed.deactivate()

    def testSingleJobReindexing(self):
        """Asserts re-indexing links job and schedule successfully."""
        priority = "top"
        test_name = "test/test"
        period = 360
        build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        manifest_branch = "manifest_branch"
        build_target = "device_build_target-user"
        pab_account_id = "1234567890"
        shards = 1
        retry_count = 2
        gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        gsi_branch = "gsi_branch"
        gsi_build_target = "gsi_build_target-user"
        gsi_pab_account_id = "1234567890"
        test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        test_branch = "gsi_branch"
        test_build_target = "gsi_build_target-user"
        test_pab_account_id = "1234567890"
        print("\n")

        print("Creating a single schedule...")
        schedule = model.ScheduleModel()
        schedule.priority = priority
        schedule.test_name = test_name
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
        schedule.put()

        schedules = model.ScheduleModel.query().fetch()
        self.assertEqual(1, len(schedules))

        print("Creating a job for stored schedule...")
        for schedule in schedules:
            job = model.JobModel()
            job.priority = schedule.priority
            job.test_name = schedule.test_name
            job.period = schedule.period
            job.build_storage_type = schedule.build_storage_type
            job.manifest_branch = schedule.manifest_branch
            job.build_target = schedule.build_target
            job.pab_account_id = schedule.device_pab_account_id
            job.shards = schedule.shards
            job.retry_count = schedule.retry_count
            job.gsi_storage_type = schedule.gsi_storage_type
            job.gsi_branch = schedule.gsi_branch
            job.gsi_build_target = schedule.gsi_build_target
            job.gsi_pab_account_id = schedule.gsi_pab_account_id
            job.test_storage_type = schedule.test_storage_type
            job.test_branch = schedule.test_branch
            job.test_build_target = schedule.test_build_target
            job.test_pab_account_id = schedule.test_pab_account_id
            job.put()

        jobs = model.JobModel.query().fetch()
        self.assertEqual(1, len(jobs))

        print("Seeking children jobs before re-indexing...")
        jobs = model.JobModel.query().fetch()
        for job in jobs:
            parent_key = job.parent_schedule
            self.assertIsNone(parent_key)

        print("Seeking children jobs after re-indexing...")
        self.indexing_handler.request.get = mock.MagicMock(return_value="job")
        self.indexing_handler.post()
        jobs = model.JobModel.query().fetch()
        for job in jobs:
            parent_key = job.parent_schedule
            parent_schedule = parent_key.get()
            self.assertEqual(
                True,
                ((parent_schedule.priority == job.priority) and
                 (parent_schedule.test_name == job.test_name) and
                 (parent_schedule.period == job.period) and
                 (parent_schedule.build_storage_type == job.build_storage_type)
                 and (parent_schedule.manifest_branch == job.manifest_branch)
                 and (parent_schedule.build_target == job.build_target) and
                 (parent_schedule.device_pab_account_id == job.pab_account_id)
                 and (parent_schedule.shards == job.shards) and
                 (parent_schedule.retry_count == job.retry_count) and
                 (parent_schedule.gsi_storage_type == job.gsi_storage_type) and
                 (parent_schedule.gsi_branch == job.gsi_branch) and
                 (parent_schedule.gsi_build_target == job.gsi_build_target) and
                 (parent_schedule.gsi_pab_account_id == job.gsi_pab_account_id)
                 and
                 (parent_schedule.test_storage_type == job.test_storage_type)
                 and (parent_schedule.test_branch == job.test_branch) and
                 (parent_schedule.test_build_target == job.test_build_target)
                 and (parent_schedule.test_pab_account_id ==
                      job.test_pab_account_id)))

    def testMultiJobReindexing(self):
        """Asserts re-indexing links job and schedule successfully."""
        priority = "top"
        test_name = ""
        period = 360
        build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        manifest_branch = "manifest_branch"
        build_target = "device_build_target-user"
        pab_account_id = "1234567890"
        shards = 1
        retry_count = 2
        gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        gsi_branch = "gsi_branch"
        gsi_build_target = "gsi_build_target-user"
        gsi_pab_account_id = "1234567890"
        test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        test_branch = "gsi_branch"
        test_build_target = "gsi_build_target-user"
        test_pab_account_id = "1234567890"
        print("\n")

        print("Creating four schedules...")
        for num in xrange(4):
            schedule = model.ScheduleModel()
            schedule.priority = priority
            schedule.test_name = test_name + str(num + 1)
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
            schedule.put()

        schedules = model.ScheduleModel.query().fetch()
        self.assertEqual(4, len(schedules))

        print("Creating jobs as number of test_name...")
        for schedule in schedules:
            for _ in xrange(int(schedule.test_name)):
                job = model.JobModel()
                job.priority = schedule.priority
                job.test_name = schedule.test_name
                job.period = schedule.period
                job.build_storage_type = schedule.build_storage_type
                job.manifest_branch = schedule.manifest_branch
                job.build_target = schedule.build_target
                job.pab_account_id = schedule.device_pab_account_id
                job.shards = schedule.shards
                job.retry_count = schedule.retry_count
                job.gsi_storage_type = schedule.gsi_storage_type
                job.gsi_branch = schedule.gsi_branch
                job.gsi_build_target = schedule.gsi_build_target
                job.gsi_pab_account_id = schedule.gsi_pab_account_id
                job.test_storage_type = schedule.test_storage_type
                job.test_branch = schedule.test_branch
                job.test_build_target = schedule.test_build_target
                job.test_pab_account_id = schedule.test_pab_account_id
                job.put()

        jobs = model.JobModel.query().fetch()
        self.assertEqual(10, len(jobs))

        print("Seeking children jobs before re-indexing...")
        jobs = model.JobModel.query().fetch()
        for job in jobs:
            parent_key = job.parent_schedule
            self.assertIsNone(parent_key)

        print("Seeking children jobs after re-indexing...")
        self.indexing_handler.request.get = mock.MagicMock(return_value="job")
        self.indexing_handler.post()
        jobs = model.JobModel.query().fetch()
        for job in jobs:
            parent_key = job.parent_schedule
            parent_schedule = parent_key.get()
            self.assertEqual(
                True,
                ((parent_schedule.priority == job.priority) and
                 (parent_schedule.test_name == job.test_name) and
                 (parent_schedule.period == job.period) and
                 (parent_schedule.build_storage_type == job.build_storage_type)
                 and (parent_schedule.manifest_branch == job.manifest_branch)
                 and (parent_schedule.build_target == job.build_target) and
                 (parent_schedule.device_pab_account_id == job.pab_account_id)
                 and (parent_schedule.shards == job.shards) and
                 (parent_schedule.retry_count == job.retry_count) and
                 (parent_schedule.gsi_storage_type == job.gsi_storage_type) and
                 (parent_schedule.gsi_branch == job.gsi_branch) and
                 (parent_schedule.gsi_build_target == job.gsi_build_target) and
                 (parent_schedule.gsi_pab_account_id == job.gsi_pab_account_id)
                 and
                 (parent_schedule.test_storage_type == job.test_storage_type)
                 and (parent_schedule.test_branch == job.test_branch) and
                 (parent_schedule.test_build_target == job.test_build_target)
                 and (parent_schedule.test_pab_account_id ==
                      job.test_pab_account_id)))


if __name__ == "__main__":
    unittest.main()
