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

import endpoints

from protorpc import remote

from webapp.src.proto import model


JOB_QUEUE_RESOURCE = endpoints.ResourceContainer(
    model.JobMessage)


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
        job_message.status = ""
        job_message.period = 0

        for job in existing_jobs:
            if job.hostname == request.hostname and job.build_id != "":
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

                return model.JobLeaseResponse(
                    return_code=model.ReturnCodeMessage.SUCCESS,
                    jobs=[job_message])

        return model.JobLeaseResponse(
            return_code=model.ReturnCodeMessage.FAIL,
            jobs=[job_message])
