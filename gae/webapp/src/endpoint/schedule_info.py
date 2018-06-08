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

from webapp.src import vtslab_status as Status
from webapp.src.proto import model

SCHEDULE_INFO_RESOURCE = endpoints.ResourceContainer(model.ScheduleInfoMessage)


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
            model.ScheduleModel.schedule_type != "green")
        existing_schedules = schedule_query.fetch(keys_only=True)
        if existing_schedules and len(existing_schedules) > 0:
            ndb.delete_multi(existing_schedules)
        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)

    @endpoints.method(
        SCHEDULE_INFO_RESOURCE,
        model.DefaultResponse,
        path="set",
        http_method="POST",
        name="set")
    def set(self, request):
        """Sets the schedule info based on `request`."""
        request_fields = request.all_fields()
        model_attrs = model.ScheduleModel.__dict__.items()
        model_attr_names = [
            x[0] for x in model_attrs if not x[0].startswith("_")
        ]
        exist_on_both = [
            x for x in request_fields if x.name in model_attr_names
        ]
        # check duplicates
        exclusions = [
            "name", "schedule_type", "schedule", "param", "timestamp",
            "children_jobs", "error_count", "suspended"
        ]
        # list of protorpc message fields.
        duplicate_checklist = [
            x for x in exist_on_both if x.name not in exclusions
        ]
        empty_list_field = []
        query = model.ScheduleModel.query()
        for field in duplicate_checklist:
            if field.repeated:
                value = request.get_assigned_value(field.name)
                if value:
                    query = query.filter(
                        getattr(model.ScheduleModel, field.name).IN(
                            request.get_assigned_value(field.name)))
                else:
                    # empty list cannot be queried.
                    empty_list_field.append(field.name)
            else:
                query = query.filter(
                    getattr(model.ScheduleModel, field.name) ==
                    request.get_assigned_value(field.name))
        duplicated_schedules = query.fetch()

        if empty_list_field:
            duplicated_schedules = [
                schedule for schedule in duplicated_schedules
                if all(
                    [not getattr(schedule, attr) for attr in empty_list_field])
            ]

        if not duplicated_schedules:
            schedule = model.ScheduleModel()
            for field in exist_on_both:
                setattr(schedule, field.name,
                        request.get_assigned_value(field.name))
            schedule.timestamp = datetime.datetime.now()
            schedule.schedule_type = "test"
            schedule.error_count = 0
            schedule.suspended = False
            schedule.priority_value = Status.GetPriorityValue(schedule.priority)
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
            model.ScheduleModel.schedule_type == "green")
        existing_schedules = schedule_query.fetch(keys_only=True)
        if existing_schedules and len(existing_schedules) > 0:
            ndb.delete_multi(existing_schedules)
        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)

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
