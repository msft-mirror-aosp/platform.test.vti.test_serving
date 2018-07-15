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
import random
import string
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from webapp.src import vtslab_status as Status
from webapp.src.proto import model


class UnitTestBase(unittest.TestCase):
    """Base class for unittest.

    Attributes:
        testbed: A Testbed instance which provides local unit testing.
        random_strs: a list of strings generated by GetRandomString() method
                     in order to avoid duplicates.
    """
    random_strs = []

    def setUp(self):
        """Initializes unittest."""
        # Create the Testbed class instance and initialize service stubs.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_mail_stub()
        self.testbed.setup_env(app_id="vtslab-schedule-unittest")
        # Clear cache between tests.
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def GetRandomString(self, length=7):
        """Generates and returns a random string.

        Args:
            length: an integer, string length.

        Returns:
            a random string.
        """
        new_str = ""
        while new_str == "" or new_str in self.random_strs:
            new_str = "".join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(length))
        return new_str

    def GenerateLabModel(self, lab_name=None, host_name=None):
        """Builds model.LabModel with given information.

        Args:
            lab_name: a string, lab name.
            host_name: a string, host name.

        Returns:
            model.LabModel instance.
        """
        lab = model.LabModel()
        lab.name = lab_name if lab_name else self.GetRandomString()
        lab.hostname = host_name if host_name else self.GetRandomString()
        lab.owner = "test@abc.com"
        lab.ip = "100.100.100.100"
        return lab

    def GenerateDeviceModel(
            self,
            status=Status.DEVICE_STATUS_DICT["fastboot"],
            scheduling_status=Status.DEVICE_SCHEDULING_STATUS_DICT["free"],
            **kwargs):
        """Builds model.DeviceModel with given information.

        Args:
            status: an integer, device's initial status.
            scheduling_status: an integer, device's initial scheduling status.
            **kwargs: the optional arguments.

        Returns:
            model.DeviceModel instance.
        """
        device = model.DeviceModel()
        device.status = status
        device.scheduling_status = scheduling_status
        device.timestamp = datetime.datetime.now()

        for arg in device._properties:
            if arg in ["status", "scheduling_status", "timestamp"]:
                continue
            if arg in kwargs:
                value = kwargs[arg]
            elif isinstance(device._properties[arg], ndb.StringProperty):
                value = self.GetRandomString()
            elif isinstance(device._properties[arg], ndb.IntegerProperty):
                value = 0
            elif isinstance(device._properties[arg], ndb.BooleanProperty):
                value = False
            else:
                print("A type of property '{}' is not supported.".format(arg))
                continue
            if device._properties[arg]._repeated:
                value = [value]
            setattr(device, arg, value)
        return device

    def GenerateScheduleModel(
            self,
            device_model=None,
            lab_model=None,
            priority="medium",
            period=360,
            retry_count=1,
            shards=1,
            lab_name=None,
            device_storage_type=Status.STORAGE_TYPE_DICT["PAB"],
            device_branch=None,
            device_target=None,
            gsi_storage_type=Status.STORAGE_TYPE_DICT["PAB"],
            gsi_build_target=None,
            test_storage_type=Status.STORAGE_TYPE_DICT["PAB"],
            test_build_target=None,
            required_signed_device_build=False,
            **kwargs):
        """Builds model.ScheduleModel with given information.

        Args:
            device_model: a model.DeviceModel instance to refer device product.
            lab_model: a model.LabModel instance to refer host name.
            priority: a string, scheduling priority
            period: an integer, scheduling period.
            retry_count: an integer, scheduling retry count.
            shards: an integer, # ways of device shards.
            lab_name: a string, target lab name.
            device_storage_type: an integer, device storage type
            device_branch: a string, device build branch.
            device_target: a string, device build target.
            gsi_storage_type: an integer, GSI storage type
            gsi_build_target: a string, GSI build target.
            test_storage_type: an integer, test storage type
            test_build_target: a string, test build target.
            required_signed_device_build: a boolean, True to schedule for signed
                                          device build, False if not.
            **kwargs: the optional arguments.

        Returns:
            model.ScheduleModel instance.
        """

        if device_model:
            device_product = device_model.product
            device_target = self.GetRandomString(4)
        elif device_target:
            device_product, device_target = device_target.split("-")
        else:
            device_product = self.GetRandomString(7)
            device_target = self.GetRandomString(4)

        if lab_model:
            lab = lab_model.name
        elif lab_name:
            lab = lab_name
        else:
            lab = self.GetRandomString()

        schedule = model.ScheduleModel()
        schedule.priority = priority
        schedule.priority_value = Status.GetPriorityValue(schedule.priority)
        schedule.period = period
        schedule.shards = shards
        schedule.retry_count = retry_count
        schedule.required_signed_device_build = required_signed_device_build
        schedule.build_storage_type = device_storage_type
        schedule.manifest_branch = (device_branch if device_branch else
                                    self.GetRandomString())
        schedule.build_target = "-".join([device_product, device_target])

        schedule.gsi_storage_type = gsi_storage_type
        schedule.gsi_build_target = (gsi_build_target
                                     if gsi_build_target else "-".join([
                                         self.GetRandomString(),
                                         self.GetRandomString(4)
                                     ]))
        schedule.test_storage_type = test_storage_type
        schedule.test_build_target = (test_build_target
                                      if test_build_target else "-".join([
                                          self.GetRandomString(),
                                          self.GetRandomString(4)
                                      ]))
        schedule.device = []
        schedule.device.append("/".join([lab, device_product]))

        for arg in schedule._properties:
            if arg in [
                    "priority", "priority_value", "period", "shards",
                    "retry_count", "required_signed_device_build",
                    "build_storage_type", "manifest_branch", "build_target",
                    "gsi_storage_type", "gsi_build_target",
                    "test_storage_type", "test_build_target", "device",
                    "children_jobs", "timestamp", "required_host_equipment",
                    "required_device_equipment"
            ]:
                continue
            if arg in kwargs:
                value = kwargs[arg]
            elif isinstance(schedule._properties[arg], ndb.StringProperty):
                value = self.GetRandomString()
            elif isinstance(schedule._properties[arg], ndb.IntegerProperty):
                value = 0
            elif isinstance(schedule._properties[arg], ndb.BooleanProperty):
                value = False
            else:
                print("A type of property '{}' is not supported.".format(arg))
                continue
            if schedule._properties[arg]._repeated:
                value = [value]
            setattr(schedule, arg, value)

        return schedule

    def GenerateBuildModel(self, schedule, targets=None):
        """Builds model.BuildModel with given information.

        Args:
            schedule: a model.ScheduleModel instance to look up build info.
            targets: a list of strings which indicates artifact type.

        Returns:
            model.BuildModel instance.
        """
        build_dict = {}
        if targets is None:
            targets = ["device", "gsi", "test"]
        for target in targets:
            build = model.BuildModel()
            build.artifact_type = target
            build.timestamp = datetime.datetime.now()
            if target == "device":
                build.signed = schedule.required_signed_device_build
                build.manifest_branch = schedule.manifest_branch
                build.build_target, build.build_type = (
                    schedule.build_target.split("-"))
            elif target == "gsi":
                build.manifest_branch = schedule.gsi_branch
                build.build_target, build.build_type = (
                    schedule.gsi_build_target.split("-"))
            elif target == "test":
                build.manifest_branch = schedule.test_branch
                build.build_target, build.build_type = (
                    schedule.test_build_target.split("-"))
            build.build_id = self.GetNewBuildId(build)
            build_dict[target] = build
        return build_dict

    def GetNewBuildId(self, build):
        """Generates build ID.

        This method always generates newest (higher number) build ID than other
        builds stored in testbed datastore.

        Args:
            build: a model.BuildModel instance to look up build information
                   from testbed datastore.

        Returns:
            a string, build ID.
        """
        format_string = "{0:07d}"
        build_query = model.BuildModel.query(
            model.BuildModel.artifact_type == build.artifact_type,
            model.BuildModel.build_target == build.build_target,
            model.BuildModel.signed == build.signed,
            model.BuildModel.manifest_branch == build.manifest_branch)
        exiting_builds = build_query.fetch()
        if exiting_builds:
            exiting_builds.sort(key=lambda x: x.build_id, reverse=True)
            latest_build_id = int(exiting_builds[0].build_id)
            return format_string.format(latest_build_id + 1)
        else:
            return format_string.format(1)

    def PassTime(self, hours=0, minutes=0, seconds=0):
        """Assumes that a certain amount of time has passed.

        This method changes does not change actual system time but changes all
        jobs timestamp to assume time has passed.

        Args:
            hours: an integer, number of hours to pass time.
            minutes: an integer, number of minutes to pass time.
            seconds: an integer, number of seconds to pass time.
        """
        if not hours and not minutes and not seconds:
            return

        jobs = model.JobModel.query().fetch()
        to_put = []
        for job in jobs:
            if job.timestamp:
                job.timestamp -= datetime.timedelta(
                    hours=hours, minutes=minutes, seconds=seconds)
            if job.heartbeat_stamp:
                job.heartbeat_stamp -= datetime.timedelta(
                    hours=hours, minutes=minutes, seconds=seconds)
            to_put.append(job)
        if to_put:
            ndb.put_multi(to_put)

    def ResetDevices(self):
        """Resets all devices to ready status."""
        devices = model.DeviceModel.query().fetch()
        to_put = []
        for device in devices:
            device.status = Status.DEVICE_STATUS_DICT["fastboot"]
            device.scheduling_status = Status.DEVICE_SCHEDULING_STATUS_DICT[
                "free"]
            to_put.append(device)
        if to_put:
            ndb.put_multi(to_put)
