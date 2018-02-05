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
from webapp.src import vtslab_status as Status


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
            if job.status == Status.JOB_STATUS_DICT["leased"]:
                status = Status.DEVICE_SCHEDULING_STATUS_DICT["use"]
            elif job.status == Status.JOB_STATUS_DICT["ready"]:
                status = Status.DEVICE_SCHEDULING_STATUS_DICT["reserved"]
            else:
                status = Status.DEVICE_SCHEDULING_STATUS_DICT["free"]
            device.scheduling_status = status
            device.put()

