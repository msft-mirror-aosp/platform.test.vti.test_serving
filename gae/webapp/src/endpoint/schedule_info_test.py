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
from webapp.src.endpoint import schedule_info
from webapp.src.proto import model
from webapp.src.testing import unittest_base


class ScheduleInfoTest(unittest_base.UnitTestBase):
    """A class to test schedule_info endpoint API.

    Attributes:
        scheduler: A mock schedule_worker.ScheduleHandler.
    """

    def setUp(self):
        """Initializes test"""
        super(ScheduleInfoTest, self).setUp()

    def testSetWithSimpleMessage(self):
        """Asserts schedule_info/set API receives a simple message."""
        # As of June 8, 2018, these are uploaded from host controller.
        message = model.ScheduleInfoMessage()
        message.manifest_branch = self.GetRandomString()
        message.build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.build_target = self.GetRandomString()
        message.require_signed_device_build = False
        message.has_bootloader_img = True
        message.has_radio_img = True
        message.test_name = self.GetRandomString()
        message.period = 360
        message.priority = "high"
        message.device = [self.GetRandomString()]
        message.required_host_equipment = [self.GetRandomString()]
        message.required_device_equipment = [self.GetRandomString()]
        message.device_pab_account_id = self.GetRandomString()
        message.shards = 1
        message.param = [self.GetRandomString()]
        message.retry_count = 1
        message.gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.gsi_branch = self.GetRandomString()
        message.gsi_build_target = self.GetRandomString()
        message.gsi_pab_account_id = self.GetRandomString()
        message.gsi_vendor_version = self.GetRandomString()
        message.test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.test_branch = self.GetRandomString()
        message.test_build_target = self.GetRandomString()
        message.test_pab_account_id = self.GetRandomString()
        # message.image_package_repo_base = self.GetRandomString()

        container = (
            schedule_info.SCHEDULE_INFO_RESOURCE.combined_message_class())
        api = schedule_info.ScheduleInfoApi()
        response = api.set(container)

        self.assertTrue(response.return_code, model.ReturnCodeMessage.SUCCESS)

    def testSetWithEmptyRepeatedField(self):
        """Asserts schedule_info/set API receives a message.

        This test sets required_host_equipment to empty and sends to endpoint
        method.
        """
        # As of June 8, 2018, these are uploaded from host controller.
        message = model.ScheduleInfoMessage()
        message.manifest_branch = self.GetRandomString()
        message.build_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.build_target = self.GetRandomString()
        message.require_signed_device_build = False
        message.has_bootloader_img = True
        message.has_radio_img = True
        message.test_name = self.GetRandomString()
        message.period = 360
        message.priority = "high"
        message.device = [self.GetRandomString()]
        message.required_host_equipment = []
        message.required_device_equipment = [self.GetRandomString()]
        message.device_pab_account_id = self.GetRandomString()
        message.shards = 1
        message.param = [self.GetRandomString()]
        message.retry_count = 1
        message.gsi_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.gsi_branch = self.GetRandomString()
        message.gsi_build_target = self.GetRandomString()
        message.gsi_pab_account_id = self.GetRandomString()
        message.gsi_vendor_version = self.GetRandomString()
        message.test_storage_type = Status.STORAGE_TYPE_DICT["PAB"]
        message.test_branch = self.GetRandomString()
        message.test_build_target = self.GetRandomString()
        message.test_pab_account_id = self.GetRandomString()
        # message.image_package_repo_base = self.GetRandomString()

        container = (
            schedule_info.SCHEDULE_INFO_RESOURCE.combined_message_class())
        api = schedule_info.ScheduleInfoApi()
        response = api.set(container)

        self.assertTrue(response.return_code, model.ReturnCodeMessage.SUCCESS)


if __name__ == "__main__":
    unittest.main()
