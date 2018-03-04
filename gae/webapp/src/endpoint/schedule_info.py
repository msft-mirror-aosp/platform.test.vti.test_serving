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

"""Schedule Info APIs implemented using Google Cloud Endpoints."""

import datetime
import endpoints

from protorpc import remote

from google.appengine.ext import ndb

from webapp.src.proto import model


SCHEDULE_INFO_RESOURCE = endpoints.ResourceContainer(
    model.ScheduleInfoMessage)


@endpoints.api(name="schedule_info", version="v1")
class ScheduleInfoApi(remote.Service):
    """Endpoint API for schedule_info."""

    @endpoints.method(
        SCHEDULE_INFO_RESOURCE,
        model.DefaultResponse,
        path="clear",
        http_method="POST",
        name="clear")
    def clear(self, request):
        """Clears schedule info in DB."""
        schedlue_query = model.ScheduleModel.query()
        existing_schedules = schedlue_query.fetch(keys_only=True)
        if existing_schedules and len(existing_schedules) > 0:
            ndb.delete_multi(existing_schedules)
        return model.DefaultResponse(return_code=model.ReturnCodeMessage.SUCCESS)

    @endpoints.method(
        SCHEDULE_INFO_RESOURCE,
        model.DefaultResponse,
        path="set",
        http_method="POST",
        name="set")
    def set(self, request):
        """Sets the schedule info based on `request`."""
        schedule = model.ScheduleModel()
        schedule.manifest_branch = request.manifest_branch
        schedule.build_target = request.build_target
        schedule.test_name = request.test_name
        schedule.period = request.period
        schedule.priority = request.priority
        schedule.device = []
        schedule.device.append(request.device)
        schedule.shards = request.shards
        schedule.param = request.param
        schedule.retry_count = request.retry_count
        schedule.gsi_branch = request.gsi_branch
        schedule.gsi_build_target = request.gsi_build_target
        schedule.gsi_pab_account_id = request.gsi_pab_account_id
        schedule.test_branch = request.test_branch
        schedule.test_build_target = request.test_build_target
        schedule.test_pab_account_id = request.test_pab_account_id
        schedule.timestamp = datetime.datetime.now()
        schedule.put()

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)
