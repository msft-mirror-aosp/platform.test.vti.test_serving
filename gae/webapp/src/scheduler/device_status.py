# Copyright 2018 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from webapp.src.proto import model

# Status dict updated from HC.
DEVICE_STATUS_DICT = {
    # default state, currently not in use.
    "unknown": 0,
    # for devices detected via "fastboot devices" shell command.
    "fastboot": 1,
    # for devices detected via "adb devices" shell command.
    "online": 2,
    # currently not in use.
    "ready": 3,
    # currently not in use.
    "use": 4,
    # for devices in error state.
    "error": 5,
    # for devices which timed out (not detected either via fastboot or adb).
    "no-response": 6
}

# Scheduling status dict based on the status of each jobs in job queue.
DEVICE_SCHEDULING_STATUS_DICT = {
    # for devices detected but not scheduled.
    "free": 0,
    # for devices scheduled but not running.
    "reserved": 1,
    # for devices scheduled for currently leased job(s).
    "use": 2
}


def RefreshDevicesScheduleingStatus(job):
    """Sets scheduling info of devices.

    changes devices_scheduling status of devices related to 'job'.

    Args
        job: Datastore job entity. Used to check whether a device is related
             to this job or not.
    """
    device_query = model.DeviceModel.query()
    devices = device_query.fetch()

    for device in devices:
        if device.serial in job.serial:
            if job.status == "LEASED":
                status = DEVICE_SCHEDULING_STATUS_DICT["use"]
            elif job.status == "READY":
                status = DEVICE_SCHEDULING_STATUS_DICT["reserved"]
            else:
                status = DEVICE_SCHEDULING_STATUS_DICT["free"]
            device.scheduling_status = status
            device.put()
