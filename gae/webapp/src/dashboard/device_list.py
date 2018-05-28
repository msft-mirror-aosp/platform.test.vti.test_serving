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

from webapp.src.handlers import base
from webapp.src.proto import model
from webapp.src import vtslab_status
from webapp.src.dashboard import device_stats


class DevicePage(base.BaseHandler):
    """Main class for /device web page."""

    def get(self):
        """Generates an HTML page based on the device info kept in DB."""
        self.template = "device.html"

        device_query = model.DeviceModel.query()
        devices = device_query.fetch()

        lab_query = model.LabModel.query()
        labs = lab_query.fetch()

        stats = device_stats.DeviceStats()
        if devices:
            devices = sorted(
                devices, key=lambda x: (x.hostname, x.product, x.status),
                reverse=False)
            for device in devices:
                device_product_lowcase = device.product.lower()
                if device.scheduling_status == vtslab_status.DEVICE_SCHEDULING_STATUS_DICT["free"]:
                    if (device.status == vtslab_status.DEVICE_STATUS_DICT["error"]
                        or device.status == vtslab_status.DEVICE_STATUS_DICT["no-response"]):
                        stats.add_error(device_product_lowcase)
                    else:
                        # it shouldn't be in use state.
                        stats.add_idle(device_product_lowcase)
                else:
                    # includes both use and reserved
                    stats.add_active(device_product_lowcase)

        template_values = {
            "devices": devices,
            "labs": labs,
            "stats": stats
        }

        self.render(template_values)
