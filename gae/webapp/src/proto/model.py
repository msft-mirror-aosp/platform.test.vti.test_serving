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

from google.appengine.ext import ndb

from protorpc import messages


class BuildModel(ndb.Model):
    """A model for representing an individual build entry."""
    manifest_branch = ndb.StringProperty(indexed=False)
    build_id = ndb.StringProperty(indexed=False)
    build_target = ndb.StringProperty(indexed=False)
    build_type = ndb.StringProperty(indexed=False)
    artifact_type = ndb.StringProperty(indexed=False)
    artifacts = ndb.StringProperty(indexed=False, repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now=False, indexed=False)


class BuildInfoMessage(messages.Message):
    """A message for representing an individual build entry."""
    manifest_branch = messages.StringField(1)
    build_id = messages.StringField(2)
    build_target = messages.StringField(3)
    build_type = messages.StringField(4)
    artifact_type = messages.StringField(5)
    artifacts = messages.StringField(6, repeated=True)


class ScheduleModel(ndb.Model):
    """A model for representing an individual schedule entry."""
    manifest_branch = ndb.StringProperty(indexed=False)
    build_target = ndb.StringProperty(indexed=False, repeated=True)  # type:name
    test_name = ndb.StringProperty(indexed=False)
    period = ndb.IntegerProperty(indexed=False)
    priority = ndb.StringProperty(indexed=False)
    device = ndb.StringProperty(indexed=False)
    shards = ndb.IntegerProperty(indexed=False)
    param = ndb.StringProperty(indexed=False, repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now=False, indexed=False)


class ScheduleInfoMessage(messages.Message):
    """A message for representing an individual schedule entry."""
    manifest_branch = messages.StringField(1)
    build_target = messages.StringField(2, repeated=True)
    test_name = messages.StringField(3)
    period = messages.IntegerField(4)
    priority = messages.StringField(5)
    device = messages.StringField(6)
    shards = messages.IntegerField(7)
    param = messages.StringField(8, repeated=True)


class LabModel(ndb.Model):
    """A model for representing an individual lab entry."""
    name = ndb.StringProperty(indexed=False)
    owner = ndb.StringProperty(indexed=False)
    hostname = ndb.StringProperty(indexed=False)
    ip = ndb.StringProperty(indexed=False)
    # devices is a comma-separated list of serial=product pairs
    devices = ndb.StringProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(auto_now=False, indexed=False)


class LabDeviceInfoMessage(messages.Message):
    """A message for representing an individual lab host's device entry."""
    serial = messages.StringField(1, repeated=False)
    product = messages.StringField(2, repeated=False)


class LabHostInfoMessage(messages.Message):
    """A message for representing an individual lab's host entry."""
    hostname = messages.StringField(1, repeated=False)
    ip = messages.StringField(2, repeated=False)
    script = messages.StringField(3)
    device = messages.MessageField(
        LabDeviceInfoMessage, 4, repeated=True)


class LabInfoMessage(messages.Message):
    """A message for representing an individual lab entry."""
    name = messages.StringField(1)
    owner = messages.StringField(2)
    host = messages.MessageField(
        LabHostInfoMessage, 3, repeated=True)


class DeviceModel(ndb.Model):
    """A model for representing an individual device entry."""
    hostname = ndb.StringProperty(indexed=False)
    product = ndb.StringProperty(indexed=False)
    serial = ndb.StringProperty(indexed=False)
    status = ndb.IntegerProperty(indexed=False)
    scheduling_status = ndb.IntegerProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(auto_now=False, indexed=False)


class DeviceInfoMessage(messages.Message):
    """A message for representing an individual host's device entry."""
    serial = messages.StringField(1)
    product = messages.StringField(2)
    status = messages.IntegerField(3)
    scheduling_status = messages.IntegerField(4)


class HostInfoMessage(messages.Message):
    """A message for representing an individual host entry."""
    hostname = messages.StringField(1)
    devices = messages.MessageField(
        DeviceInfoMessage, 2, repeated=True)


class JobModel(ndb.Model):
    """A model for representing an individual job entry."""
    hostname = ndb.StringProperty(indexed=False)
    priority = ndb.StringProperty(indexed=False)
    test_name = ndb.StringProperty(indexed=False)
    device = ndb.StringProperty(indexed=False)
    serial = ndb.StringProperty(indexed=False, repeated=True)
    manifest_branch = ndb.StringProperty(indexed=False)
    build_target = ndb.StringProperty(indexed=False, repeated=True)
    shards = ndb.IntegerProperty(indexed=False)
    param = ndb.StringProperty(indexed=False, repeated=True)
    build_id = ndb.StringProperty(indexed=False)
    status = ndb.IntegerProperty(indexed=False)
    period = ndb.IntegerProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(auto_now=False, indexed=False)


class JobMessage(messages.Message):
    """A message for representing an individual job entry."""
    hostname = messages.StringField(1)
    priority = messages.StringField(2)
    test_name = messages.StringField(3)
    device = messages.StringField(4)
    serial = messages.StringField(5, repeated=True)
    manifest_branch = messages.StringField(6)
    build_target = messages.StringField(7, repeated=True)
    shards = messages.IntegerField(8)
    param = messages.StringField(9, repeated=True)
    build_id = messages.StringField(10)
    status = messages.IntegerField(11)
    period = messages.IntegerField(12)


class ReturnCodeMessage(messages.Enum):
    """Enum for default return code."""
    SUCCESS = 0
    FAIL = 1


class DefaultResponse(messages.Message):
    """A default response proto message."""
    return_code = messages.EnumField(ReturnCodeMessage, 1)


class JobLeaseResponse(messages.Message):
    """A job lease response proto message."""
    return_code = messages.EnumField(ReturnCodeMessage, 1)
    jobs = messages.MessageField(JobMessage, 2, repeated=True)
