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

from webapp.src.endpoint import endpoint_base
from webapp.src.proto import model
from webapp.src.testing import unittest_base


class EndpointBaseTest(unittest_base.UnitTestBase):
    """A class to test endpoint_base.EndpointBase class. """

    def setUp(self):
        """Initializes test"""
        super(EndpointBaseTest, self).setUp()

    def testGetAssignedMessagesAttributes(self):
        attrs = ["hostname", "priority", "test_branch"]
        job_message = model.JobMessage()
        for attr in attrs:
            setattr(job_message, attr, attr)
        eb = endpoint_base.EndpointBase()
        result = eb.GetAttributes(job_message, assigned_only=True)
        self.assertEquals(set(attrs), set(result))

    def testGetAssignedModelAttributes(self):
        attrs = ["hostname", "priority", "test_branch"]
        job = model.JobModel()
        for attr in attrs:
            setattr(job, attr, attr)
        eb = endpoint_base.EndpointBase()
        result = eb.GetAttributes(job, assigned_only=True)
        self.assertEquals(set(attrs), set(result))

    def testGetAllMessagesAttributes(self):
        attrs = ["hostname", "priority", "test_branch"]
        full_attrs = [
            "test_type", "hostname", "priority", "test_name",
            "require_signed_device_build", "has_bootloader_img",
            "has_radio_img", "device", "serial", "build_storage_type",
            "manifest_branch", "build_target", "build_id", "pab_account_id",
            "shards", "param", "status", "period", "gsi_storage_type",
            "gsi_branch", "gsi_build_target", "gsi_build_id",
            "gsi_pab_account_id", "gsi_vendor_version", "test_storage_type",
            "test_branch", "test_build_target", "test_build_id",
            "test_pab_account_id", "retry_count", "infra_log_url",
            "image_package_repo_base", "report_bucket", "report_spreadsheet_id"
        ]
        job_message = model.JobMessage()
        for attr in attrs:
            setattr(job_message, attr, attr)
        eb = endpoint_base.EndpointBase()
        result = eb.GetAttributes(job_message, assigned_only=False)
        self.assertTrue(set(full_attrs) <= set(result))

    def testGetAllModelAttributes(self):
        attrs = ["hostname", "priority", "test_branch"]
        full_attrs = [
            "test_type", "hostname", "priority", "test_name",
            "require_signed_device_build", "has_bootloader_img",
            "has_radio_img", "device", "serial", "build_storage_type",
            "manifest_branch", "build_target", "build_id", "pab_account_id",
            "shards", "param", "status", "period", "gsi_storage_type",
            "gsi_branch", "gsi_build_target", "gsi_build_id",
            "gsi_pab_account_id", "gsi_vendor_version", "test_storage_type",
            "test_branch", "test_build_target", "test_build_id",
            "test_pab_account_id", "timestamp", "heartbeat_stamp",
            "retry_count", "infra_log_url", "parent_schedule",
            "image_package_repo_base", "report_bucket", "report_spreadsheet_id"
        ]
        job = model.JobModel()
        for attr in attrs:
            setattr(job, attr, attr)
        eb = endpoint_base.EndpointBase()
        result = eb.GetAttributes(job, assigned_only=False)
        self.assertTrue(set(full_attrs) <= set(result))


if __name__ == "__main__":
    unittest.main()
