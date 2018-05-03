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

from webapp.src.handlers import base
from webapp.src.proto import model
from webapp.src.utils import email_util


class SchedulePage(base.BaseHandler):
    """Main class for /schedule web page."""

    def get(self):
        """Generates an HTML page based on the task schedules kept in DB."""
        self.template = "schedule.html"

        resume_key = self.request.get("resume")
        if resume_key:
            schedule_key = ndb.key.Key(urlsafe=resume_key)
            schedule = schedule_key.get()
            schedule.suspended = False
            schedule.put()
            email_util.send_schedule_suspension_notification(schedule)

        suspend_key = self.request.get("suspend")
        if suspend_key:
            schedule_key = ndb.key.Key(urlsafe=suspend_key)
            schedule = schedule_key.get()
            schedule.suspended = True
            schedule.put()
            email_util.send_schedule_suspension_notification(schedule)

        toggle = self.request.get("schedule_enable_status_toggle", default_value="0")

        schedule_control = model.ScheduleControlModel.query()
        schedule_control_dataset = schedule_control.fetch()
        enabled = True
        if schedule_control_dataset:
            for schedule_control_data_tuple in schedule_control_dataset:
                if (not schedule_control_data_tuple.schedule_name or
                    schedule_control_data_tuple.schedule_name == "global"):
                    enabled = schedule_control_data_tuple.enabled
                    if toggle == "1":
                        enabled = not enabled
                        schedule_control_data_tuple.enabled = enabled
                        schedule_control_data_tuple.put()
                        toggle = "0"
                    break

        if toggle == "1":
            schedule_control_data_tuple = model.ScheduleControlModel()
            enabled = not enabled
            schedule_control_data_tuple.enabled = enabled
            schedule_control_data_tuple.put()

        schedule_query = model.ScheduleModel.query()
        schedules = schedule_query.fetch()

        if schedules:
            schedules = sorted(
                schedules, key=lambda x: (x.manifest_branch, x.build_target),
                reverse=False)

        template_values = {
            "schedules": schedules,
            "enabled": enabled
        }

        self.render(template_values)
