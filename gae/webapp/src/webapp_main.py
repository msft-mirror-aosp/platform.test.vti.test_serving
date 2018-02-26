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

import webapp2

from google.appengine.api import users

from webapp.src import webapp_config

from webapp.src.dashboard import build_list
from webapp.src.dashboard import device_list
from webapp.src.dashboard import job_list
from webapp.src.dashboard import schedule_list
from webapp.src.scheduler import periodic
from webapp.src.scheduler import device_heartbeat
from webapp.src.scheduler import job_heartbeat
from webapp.src.tasks import indexing


class MainPage(webapp2.RequestHandler):
    """Main web page request handler."""

    def get(self):
        """Generates an HTML page."""
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            "user": user,
            "url": url,
            "url_linktext": url_linktext,
        }

        template = webapp_config.JINJA_ENVIRONMENT.get_template(
            "static/index.html")
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/build", build_list.BuildPage),
    ("/device", device_list.DevicePage),
    ("/job", job_list.JobPage),
    ("/result", MainPage),
    ("/schedule", schedule_list.SchedulePage),
    ("/tasks/schedule", periodic.PeriodicScheduler),
    ("/tasks/device_heartbeat", device_heartbeat.PeriodicDeviceHeartBeat),
    ("/tasks/job_heartbeat", job_heartbeat.PeriodicJobHeartBeat),
    ("/tasks/indexing", indexing.CreateIndex)
], debug=False)
