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

from webapp.src import vtslab_status as Status
from webapp.src.dashboard import build_list
from webapp.src.proto import model


def StrGT(left, right):
    """Returns true if `left` string is greater than `right` in value."""
    if len(left) > len(right):
        right = "0" * (len(left) - len(right)) + right
    elif len(right) > len(left):
        left = "0" * (len(right) - len(left)) + left
    return left > right


class PeriodicScheduler(webapp2.RequestHandler):
    """Main class for /tasks/schedule servlet which does actual job scheduling.

    periodic scheduling.

    Attributes:
        log_message: a list of strings, containing the log messages.
    """

    log_message = []

    def ReserveDevices(self, devices, target_device_serials):
        """..."""
        for device in devices:
            if device.serial in target_device_serials:
                device.scheduling_status = Status.DEVICE_SCHEDULING_STATUS_DICT[
                    "reserved"]
                device.put()

    def FindBuildId(self, new_job, builds):
        build_id = new_job.build_id

        if builds:
            self.LogPrintln("-- Find build ID")

            for device_build in builds:
                if device_build.artifact_type != "device":
                    continue

                if (not hasattr(device_build, "build_target")
                        or not hasattr(device_build, "build_type")
                        or not hasattr(device_build, "manifest_branch")
                        or not hasattr(device_build, "build_id")):
                    self.LogPrintln(
                        "-- some field(s) missing ERROR %s" % device_build)
                    continue

                candidate_device = "-".join(
                    [device_build.build_target, device_build.build_type])
                self.LogPrintln("-- check candidate_device %s (%s)" %
                                (candidate_device, new_job.build_target[0]))
                if (device_build.manifest_branch == new_job.manifest_branch
                        and new_job.build_target[0] == candidate_device):
                    if (not build_id
                            or StrGT(device_build.build_id, build_id)):
                        build_id = device_build.build_id
        return build_id

    def get(self):
        """Generates an HTML page based on the task schedules kept in DB."""
        self.LogClear()

        schedule_query = model.ScheduleModel.query()
        schedules = schedule_query.fetch()

        lab_query = model.LabModel.query()
        labs = lab_query.fetch()

        device_query = model.DeviceModel.query()
        devices = device_query.fetch()

        job_query = model.JobModel.query()
        jobs = job_query.fetch()

        build_query = model.BuildModel.query()
        builds = build_query.fetch()

        if schedules:
            for schedule in schedules:
                self.LogPrintln("Schedule: %s" % schedule.test_name)
                self.LogIndent()
                if self.NewPeriod(schedule, jobs):
                    self.LogPrintln("- Need new job")
                    target_host, target_device_serials = self.SelectTargetLab(
                        schedule, labs, devices)
                    self.LogPrintln("- Target host: %s" % target_host)
                    self.LogPrintln(
                        "- Target serials: %s" % target_device_serials)
                    # TODO: update device status

                    # create job and add.
                    if target_host:
                        new_job = model.JobModel()
                        new_job.hostname = target_host
                        new_job.priority = schedule.priority
                        new_job.test_name = schedule.test_name
                        new_job.device = schedule.device
                        new_job.period = schedule.period
                        new_job.serial.extend(target_device_serials)
                        new_job.manifest_branch = schedule.manifest_branch
                        new_job.build_target.extend(schedule.build_target)
                        new_job.shards = schedule.shards
                        new_job.param = schedule.param
                        # assume device build
                        #_, device_builds, _ = build_list.ReadBuildInfo()

                        new_job.build_id = ""
                        new_job.build_id = self.FindBuildId(new_job, builds)
                        org_build_target = new_job.build_target[0]
                        if not new_job.build_id:
                            if new_job.build_target[0].startswith("aosp_"):
                                new_job.build_target[0] = new_job.build_target[
                                    0].replace("aosp_", "")
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)
                            else:
                                new_job.build_target[
                                    0] = "aosp_" + new_job.build_target[0]
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)

                        new_job.build_target[0] = org_build_target
                        if not new_job.build_id:
                            if new_job.build_target[0].endswith("-user"):
                                new_job.build_target[0] = new_job.build_target[
                                    0].replace("-user", "-userdebug")
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)
                            elif new_job.build_target[0].endswith(
                                    "-userdebug"):
                                new_job.build_target[0] = new_job.build_target[
                                    0].replace("-userdebug", "-user")
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)

                        if not new_job.build_id:
                            if new_job.build_target[0].startswith("aosp_"):
                                new_job.build_target[0] = new_job.build_target[
                                    0].replace("aosp_", "")
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)
                            else:
                                new_job.build_target[
                                    0] = "aosp_" + new_job.build_target[0]
                                new_job.build_id = self.FindBuildId(
                                    new_job, builds)

                        if new_job.build_id:
                            self.ReserveDevices(devices, target_device_serials)
                            # TODO remove only until full builds are available.
                            new_job.status = Status.JOB_STATUS_DICT["ready"]
                            new_job.timestamp = datetime.datetime.now()
                            new_job.put()
                            self.LogPrintln("NEW JOB")
                        else:
                            self.LogPrintln("NO BUILD FOUND")
                self.LogUnindent()

        self.response.write(
            "<pre>\n" + "\n".join(self.log_message) + "\n</pre>")

    def LogClear(self):
        """Clears the log buffer."""
        self.log_message = []
        self.log_indent = 0

    def LogPrintln(self, msg):
        """Stores a new string `msg` to the log buffer."""
        indent = "  " * self.log_indent
        self.log_message.append(indent + msg)

    def LogIndent(self):
        self.log_indent += 1

    def LogUnindent(self):
        self.log_indent -= 1

    def NewPeriod(self, schedule, jobs):
        """Checks whether a new job creation is needed.

        Args:
            schedule: a proto containing schedule information.
            jobs: a list of proto messages containing existing job information.

        Returns:
            True if new job is required, False otherwise.
        """
        if not jobs:
            return True

        def IsScheduleAndJobTheSame(schedule, job):
            return (job.manifest_branch == schedule.manifest_branch
                    and job.build_target == schedule.build_target
                    and job.test_name == schedule.test_name
                    and job.period == schedule.period
                    and job.device == schedule.device
                    and job.shards == schedule.shards
                    and job.param == schedule.param)

        latest_timestamp = None
        for job in jobs:
            if IsScheduleAndJobTheSame(schedule, job):
                #if ((job.status == "COMPLETE" or job.status == "LEASED") and
                if latest_timestamp is None:
                    latest_timestamp = job.timestamp
                elif latest_timestamp < job.timestamp:
                    latest_timestamp = job.timestamp

        if latest_timestamp is None:
            return True

        if (latest_timestamp <= (datetime.datetime.now() -
                                 datetime.timedelta(minutes=job.period))):
            return True

        return False

    def SelectTargetLab(self, schedule, labs, devices):
        """Find target host and devices to schedule a new job.

        Args:
            schedule: a proto containing the information of a schedule.
            labs: a list of proto messages containing info about available
                  labs.
            devices: a list of proto messages containing available device
                     information.

        Returns:
            hostname,
            a list of selected devices  (see whether devices will be selected later when the job is picked up.)
        """
        if "/" not in schedule.device:
            # device malformed
            return None, None

        target_lab, target_product_type = schedule.device.split("/")
        self.LogPrintln("- Seeking product %s in lab %s" %
                        (target_product_type, target_lab))
        self.LogIndent()

        available_devices = {}
        if labs and devices:
            for lab in labs:
                if lab.name != target_lab:
                    continue
                self.LogPrintln("- target lab found")
                self.LogPrintln("- target device %s %s" %
                                (lab.hostname, target_product_type))
                self.LogIndent()
                for device in devices:
                    self.LogPrintln("- check device %s %s %s" % (
                                       device.hostname, device.status,
                                       device.product))
                    if (device.hostname == lab.hostname and (device.status in [
                        Status.DEVICE_STATUS_DICT["fastboot"],
                        Status.DEVICE_STATUS_DICT["online"],
                        Status.DEVICE_STATUS_DICT["ready"]
                    ]) and (device.scheduling_status in [
                        Status.DEVICE_SCHEDULING_STATUS_DICT["free"]
                    ]) and device.product == target_product_type):
                        self.LogPrintln("- a device found %s" % device.serial)
                        if device.hostname not in available_devices:
                            available_devices[device.hostname] = []
                        available_devices[device.hostname].append(
                            device.serial)
                self.LogUnindent()
        self.LogUnindent()

        for host in available_devices:
            self.LogPrintln("- len(devices) %s > shards %s ?" %
                            (len(available_devices[host]), schedule.shards))
            if len(available_devices[host]) >= schedule.shards:
                return host, available_devices[host][:schedule.shards]

        return None, []
