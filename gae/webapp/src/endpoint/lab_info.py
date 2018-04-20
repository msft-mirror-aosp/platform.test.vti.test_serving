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

"""Lab Info APIs implemented using Google Cloud Endpoints."""

import datetime
import endpoints

from protorpc import remote

from google.appengine.ext import ndb

from webapp.src.endpoint import host_info
from webapp.src.proto import model


LAB_INFO_RESOURCE = endpoints.ResourceContainer(
    model.LabInfoMessage)
LAB_HOST_INFO_RESOURCE = endpoints.ResourceContainer(
    model.LabHostInfoMessage)


@endpoints.api(name='lab_info', version='v1')
class LabInfoApi(remote.Service):
    """Endpoint API for lab_info."""

    @endpoints.method(
        LAB_INFO_RESOURCE,
        model.DefaultResponse,
        path="clear",
        http_method="POST",
        name="clear")
    def clear(self, request):
        """Clears lab info in DB."""
        lab_query = model.LabModel.query()
        existing_labs = lab_query.fetch(keys_only=True)
        if existing_labs and len(existing_labs) > 0:
            ndb.delete_multi(existing_labs)
        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)

    @endpoints.method(
        LAB_INFO_RESOURCE,
        model.DefaultResponse,
        path="set",
        http_method="POST",
        name="set")
    def set(self, request):
        """Sets the lab info based on `request`."""
        for host in request.host:
            lab = model.LabModel()
            lab.name = request.name
            lab.owner = request.owner
            lab.admin = request.admin
            lab.hostname = host.hostname
            lab.ip = host.ip
            lab.script = host.script
            devices = []
            null_device_count = 0
            if host.device:
                for device in host.device:
                    devices.append("%s=%s" % (device.serial, device.product))
                    if device.product == "null":
                        null_device_count += 1
            if devices:
                lab.devices = ",".join(devices)
            lab.timestamp = datetime.datetime.now()
            lab.put()

            if null_device_count > 0:
                host_info.AddNullDevices(host.hostname, null_device_count)

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)

    @endpoints.method(
        LAB_HOST_INFO_RESOURCE,
        model.DefaultResponse,
        path="set_version",
        http_method="POST",
        name="set_version")
    def set_version(self, request):
        """Sets vtslab version of the host <hostname>"""
        lab_query = model.LabModel.query(
            model.LabModel.hostname == request.hostname
        )
        labs = lab_query.fetch()

        for lab in labs:
            lab.vtslab_version = request.vtslab_version.split(":")[0]
            lab.put()

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)

