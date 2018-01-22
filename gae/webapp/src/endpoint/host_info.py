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

"""Host Info APIs implemented using Google Cloud Endpoints."""

import datetime
import endpoints

from protorpc import message_types
from protorpc import remote

from google.appengine.api import users

from webapp.src.proto import model


HOST_INFO_RESOURCE = endpoints.ResourceContainer(
    model.HostInfoMessage)


@endpoints.api(name='host_info', version='v1')
class HostInfoApi(remote.Service):
    """Endpoint API for host_info."""

    @endpoints.method(
        HOST_INFO_RESOURCE,
        model.DefaultResponse,
        path='set',
        http_method='POST',
        name='set')
    def set(self, request):
        """Sets the host info based on the `request`."""
        device_query = model.DeviceModel.query()
        existing_devices = device_query.fetch()

        if users.get_current_user():
            username = users.get_current_user().email()
        else:
            username = "anonymous"

        device = model.DeviceModel()
        for request_device in request.devices:
            # it already exists.
            hit = False
            for existing_device in existing_devices:
                if request_device.serial == existing_device.serial:
                    hit = True
                    existing_device.username = username
                    existing_device.hostname = request.hostname
                    existing_device.product = request_device.product
                    existing_device.status = request_device.status
                    existing_device.scheduling_status = 0
                    existing_device.timestamp = datetime.datetime.now()
                    existing_device.put()
                    break

            if not hit:
                device = model.DeviceModel()
                device.username = username
                device.hostname = request.hostname
                device.serial = request_device.serial
                device.product = request_device.product
                device.status = request_device.status
                device.scheduling_status = 0
                device.timestamp = datetime.datetime.now()
                device.put()

        return model.DefaultResponse(
            return_code=model.ReturnCodeMessage.SUCCESS)
