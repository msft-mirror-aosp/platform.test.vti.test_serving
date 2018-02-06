# Copyright 2017 Google Inc. All rights reserved.
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
"""Job Queue Info APIs implemented using Google Cloud Endpoints."""

import datetime
import endpoints

from protorpc import remote

from google.appengine.ext import deferred

from webapp.src.proto import model
from webapp.src.scheduler import device_status
from webapp.src import vtslab_status as Status

JOB_QUEUE_RESOURCE = endpoints.ResourceContainer(model.JobMessage)

# The default timeout for leased jobs in sec.
_LEASED_JOB_RESPONSE_TIMEOUT_IN_SECS = 300

# A dict stores timestamps of the last heartbeat signal from HC
# for the leased jobs
_timestamp_last_heartbeat = {}


def SetJobStatusToReady(key):
    """Sets certain job to READY status if there is no heartbeat from HC.

    Args
        key: Datastore key for an entity.
    """
    if key.id() in _timestamp_last_heartbeat:
        current_time = datetime.datetime.now()
        if (current_time - _timestamp_last_heartbeat[key.id()]
            ).seconds >= _LEASED_JOB_RESPONSE_TIMEOUT_IN_SECS:
            job = key.get()
            if job.status == Status.JOB_STATUS_DICT["leased"]:
                job.status = Status.JOB_STATUS_DICT["ready"]
                job.put()
                device_status.RefreshDevicesScheduleingStatus(job)
            _timestamp_last_heartbeat.pop(key.id())


@endpoints.api(name='job_queue', version='v1')
class JobQueueApi(remote.Service):
    """Endpoint API for job_queue."""

    @endpoints.method(
        JOB_QUEUE_RESOURCE,
        model.JobLeaseResponse,
        path='get',
        http_method='POST',
        name='get')
    def get(self, request):
        """Gets the job(s) based on the condition specified in `request`."""
        job_query = model.JobModel.query()
        existing_jobs = job_query.fetch()

        job_message = model.JobMessage()

        job_message.hostname = ""
        job_message.priority = ""
        job_message.test_name = ""
        job_message.device = ""
        job_message.serial = [""]
        job_message.manifest_branch = ""
        job_message.build_target = [""]
        job_message.shards = 0
        job_message.param = [""]
        job_message.build_id = ""
        job_message.status = 0
        job_message.period = 0

        for job in existing_jobs:
            if (job.hostname == request.hostname and job.build_id != ""
                    and job.status == Status.JOB_STATUS_DICT["ready"]):
                job_message.hostname = job.hostname
                job_message.priority = job.priority
                job_message.test_name = job.test_name
                job_message.device = job.device
                job_message.serial = job.serial
                job_message.manifest_branch = job.manifest_branch
                job_message.build_target = job.build_target
                job_message.shards = job.shards
                job_message.param = job.param
                job_message.build_id = job.build_id
                job_message.status = job.status
                job_message.period = job.period
                job.put()
                device_status.RefreshDevicesScheduleingStatus(job)

                return model.JobLeaseResponse(
                    return_code=model.ReturnCodeMessage.SUCCESS,
                    jobs=[job_message])

        return model.JobLeaseResponse(
            return_code=model.ReturnCodeMessage.FAIL, jobs=[job_message])

    @endpoints.method(
        JOB_QUEUE_RESOURCE,
        model.JobLeaseResponse,
        path='heartbeat',
        http_method='POST',
        name='heartbeat')
    def heartbeat(self, request):
        """Processes the heartbeat signal from HC which leased queued job(s)."""
        job_query = model.JobModel.query()
        existing_jobs = job_query.fetch()

        job_message = model.JobMessage()
        job_messages = []

        for job in existing_jobs:
            if (job.serial == request.serial
                    and job.build_target == request.build_target
                    and job.manifest_branch == request.manifest_branch):
                job_message.hostname = job.hostname
                job_message.priority = job.priority
                job_message.test_name = job.test_name
                job_message.device = job.device
                job_message.serial = job.serial
                job_message.manifest_branch = job.manifest_branch
                job_message.build_target = job.build_target
                job_message.shards = job.shards
                job_message.param = job.param
                job_message.build_id = job.build_id
                job_message.status = job.status
                job_message.period = job.period
                job_messages.append(job_message)
                if job.status != Status.JOB_STATUS_DICT["leased"]:
                    return model.JobLeaseResponse(
                        return_code=model.ReturnCodeMessage.FAIL,
                        jobs=job_messages)
                self.SetJobStatus(job, request.status)

        return model.JobLeaseResponse(
            return_code=model.ReturnCodeMessage.SUCCESS, jobs=job_messages)

    def SetJobStatus(self, job, status):
        """Sets the job's status to 'status'.

        and defers SetJobStatusToReady func for checking heartbeat timeout.

        Args:
            job: Datastore object, contains job information.
            status: string, status value requested from HC.
        """
        job.status = status
        job_key = job.put()
        device_status.RefreshDevicesScheduleingStatus(job)
        _timestamp_last_heartbeat[job_key.id()] = datetime.datetime.now()
        deferred.defer(
            SetJobStatusToReady,
            job_key,
            _countdown=_LEASED_JOB_RESPONSE_TIMEOUT_IN_SECS)
