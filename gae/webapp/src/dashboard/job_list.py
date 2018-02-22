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

from webapp.src.handlers.base import BaseHandler
from webapp.src.proto import model


class JobPage(BaseHandler):
    """Main class for /job web page."""

    def get(self):
        """Generates an HTML page based on the job queue info kept in DB."""
        self.template = "job.html"

        job_query = model.JobModel.query()
        jobs = job_query.fetch()

        template_values = {
            "jobs": sorted(jobs, key=lambda x: x.timestamp, reverse=True)
        }

        self.render(template_values)
