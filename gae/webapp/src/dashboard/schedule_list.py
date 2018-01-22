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

import datetime
import webapp2

from google.appengine.api import users

from webapp.src import webapp_config
from webapp.src.dashboard import build_list
from webapp.src.proto import model


class SchedulePage(webapp2.RequestHandler):
    """Main class for /schedule web page."""

    def get(self):
        """Generates an HTML page based on the task schedules kept in DB."""
        schedule_query = model.ScheduleModel.query()
        schedules = schedule_query.fetch()

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        if schedules:
            schedules = sorted(
                schedules, key=lambda x: (x.manifest_branch, x.build_target),
                reverse=False)

        template_values = {
            "user": user,
            "schedules": schedules,
            "url": url,
            "url_linktext": url_linktext,
        }

        template = webapp_config.JINJA_ENVIRONMENT.get_template(
            "static/schedule.html")
        self.response.write(template.render(template_values))
