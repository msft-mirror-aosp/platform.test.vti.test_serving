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
        """Clears test schedule info in DB."""
        schedule_query = model.ScheduleModel.query(
            model.ScheduleModel.schedule_type != "green"
        )
        existing_schedules = schedule_query.fetch(keys_only=True)
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
        # device_pab_account_id, param are missing.
        duplicated_schedule_query = model.ScheduleModel.query(
            model.ScheduleModel.manifest_branch == request.manifest_branch,
            model.ScheduleModel.build_storage_type == request.build_storage_type,
            model.ScheduleModel.build_target == request.build_target,
            model.ScheduleModel.test_name == request.test_name,
            model.ScheduleModel.require_signed_device_build == (
                request.require_signed_device_build),
            model.ScheduleModel.period == request.period,
            model.ScheduleModel.priority == request.priority,
            model.ScheduleModel.device.IN(request.device),
            model.ScheduleModel.shards == request.shards,
            model.ScheduleModel.retry_count == request.retry_count,
            model.ScheduleModel.gsi_storage_type == request.gsi_storage_type,
            model.ScheduleModel.gsi_branch == request.gsi_branch,
            model.ScheduleModel.gsi_build_target == request.gsi_build_target,
            model.ScheduleModel.gsi_vendor_version == request.gsi_vendor_version,
            model.ScheduleModel.gsi_pab_account_id == request.gsi_pab_account_id,
            model.ScheduleModel.test_storage_type == request.test_storage_type,
            model.ScheduleModel.test_branch == request.test_branch,
            model.ScheduleModel.test_build_target == request.test_build_target,
            model.ScheduleModel.test_pab_account_id == request.test_pab_account_id
        )
        duplicated_schedules = duplicated_schedule_query.fetch()

        if not duplicated_schedules:
            schedule = model.ScheduleModel()
            schedule.manifest_branch = request.manifest_branch
            schedule.build_storage_type = request.build_storage_type
            if request.get_assigned_value("device_pab_account_id"):
                schedule.device_pab_account_id = request.device_pab_account_id
            schedule.build_target = request.build_target
            schedule.test_name = request.test_name
            schedule.require_signed_device_build = (
                request.require_signed_device_build)
            schedule.period = request.period
            schedule.priority = request.priority
            schedule.device = request.device
            schedule.shards = request.shards
            schedule.param = request.param
            schedule.retry_count = request.retry_count
            schedule.gsi_storage_type = request.gsi_storage_type
            schedule.gsi_branch = request.gsi_branch
            schedule.gsi_build_target = request.gsi_build_target
            schedule.gsi_vendor_version = request.gsi_vendor_version
            schedule.gsi_pab_account_id = request.gsi_pab_account_id
            schedule.test_storage_type = request.test_storage_type
            schedule.test_branch = request.test_branch
            schedule.test_build_target = request.test_build_target
            schedule.test_pab_account_id = request.test_pab_account_id
            schedule.timestamp = datetime.datetime.now()
            schedule.schedule_type = "test"
            schedule.error_count = 0
            schedule.suspended = False
            schedule.put()

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)


@endpoints.api(name="green_schedule_info", version="v1")
class GreenScheduleInfoApi(remote.Service):
    """Endpoint API for green_schedule_info."""

    @endpoints.method(
        SCHEDULE_INFO_RESOURCE,
        model.DefaultResponse,
        path="clear",
        http_method="POST",
        name="clear")
    def clear(self, request):
        """Clears green build schedule info in DB."""
        schedule_query = model.ScheduleModel.query(
            model.ScheduleModel.schedule_type == "green"
        )
        existing_schedules = schedule_query.fetch(keys_only=True)
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
        """Sets the green build schedule info based on `request`."""
        schedule = model.ScheduleModel()
        schedule.name = request.name
        schedule.manifest_branch = request.manifest_branch
        schedule.build_target = request.build_target
        schedule.device_pab_account_id = request.device_pab_account_id
        schedule.test_name = request.test_name
        schedule.schedule = request.schedule
        schedule.priority = request.priority
        schedule.device = request.device
        schedule.shards = request.shards
        schedule.gsi_branch = request.gsi_branch
        schedule.gsi_build_target = request.gsi_build_target
        schedule.gsi_pab_account_id = request.gsi_pab_account_id
        schedule.gsi_vendor_version = request.gsi_vendor_version
        schedule.test_branch = request.test_branch
        schedule.test_build_target = request.test_build_target
        schedule.test_pab_account_id = request.test_pab_account_id
        schedule.timestamp = datetime.datetime.now()
        schedule.schedule_type = "green"
        schedule.put()

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)
