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
from webapp.src.proto import model


def ReadBuildInfo():
    """Reads build information.

    Returns:
        a dict containing test build information,
        a dict containing device build information,
        a dict containing gsi build information.
    """
    build_query = model.BuildModel.query()
    builds = build_query.fetch()

    test_builds = []
    device_builds = []
    gsi_builds = []
    for build in builds:
        if build.artifact_type == "test":
            test_builds.append(build)
        elif build.artifact_type == "device":
            device_builds.append(build)
        elif build.artifact_type == "gsi":
            gsi_builds.append(build)
        else:
            print("unknown artifact_type %s" % build.artifact_type)

    return test_builds, device_builds, gsi_builds


class BuildPage(webapp2.RequestHandler):
    """Main class for /build web page."""

    def get(self):
        """Generates an HTML page based on the build info kept in DB."""
        test_builds, device_builds, gsi_builds = ReadBuildInfo()
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            "user": user,
            "test_builds": test_builds,
            "device_builds": device_builds,
            "gsi_builds": gsi_builds,
            "url": url,
            "url_linktext": url_linktext,
        }

        template = webapp_config.JINJA_ENVIRONMENT.get_template(
            "static/build.html")
        self.response.write(template.render(template_values))
