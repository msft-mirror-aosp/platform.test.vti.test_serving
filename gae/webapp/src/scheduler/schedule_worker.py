#!/usr/bin/env python
#
# Copyright (C) 2018 The Android Open Source Project
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
import logging
import re

from webapp.src import vtslab_status as Status
from webapp.src.proto import model
from webapp.src.utils import logger
from webapp.src.utils import model_util
import webapp2

MAX_LOG_CHARACTERS = 10000  # maximum number of characters per each log


def GetTestVersionType(manifest_branch, gsi_branch, test_type=0):
    """Compares manifest branch and gsi branch to get test type.

    This function only completes two LSBs which represent version related
    test type.

    Args:
        manifest_branch: a string, manifest branch name.
        gsi_branch: a string, gsi branch name.
        test_type: an integer, previous test type value.

    Returns:
        An integer, test type value.
    """
    if not test_type:
        value = 0
    else:
        # clear two bits
        value = test_type & ~(1 | 1 << 1)

    if not manifest_branch:
        logging.debug("manifest branch cannot be empty or None.")
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_UNKNOWN]

    if not gsi_branch:
        logging.debug("gsi_branch is empty.")
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_TOT]

    gcs_pattern = "^gs://.*/v([0-9.]*)/.*"
    p_pattern = "(git_)?p.*"
    o_mr1_pattern = "(git_)?o.*mr1.*"
    o_pattern = "(git_)?o.*"
    master_pattern = "(git_)master"

    gcs_search = re.search(gcs_pattern, manifest_branch)
    if gcs_search:
        device_version = gcs_search.group(1)
    elif re.match(p_pattern, manifest_branch):
        device_version = "9.0"
    elif re.match(o_mr1_pattern, manifest_branch):
        device_version = "8.1"
    elif re.match(o_pattern, manifest_branch):
        device_version = "8.0"
    elif re.match(master_pattern, manifest_branch):
        device_version = "master"
    else:
        logging.debug("Unknown device version.")
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_UNKNOWN]

    gcs_search = re.search(gcs_pattern, gsi_branch)
    if gcs_search:
        gsi_version = gcs_search.group(1)
    elif re.match(p_pattern, gsi_branch):
        gsi_version = "9.0"
    elif re.match(o_mr1_pattern, gsi_branch):
        gsi_version = "8.1"
    elif re.match(o_pattern, gsi_branch):
        gsi_version = "8.0"
    elif re.match(master_pattern, gsi_branch):
        gsi_version = "master"
    else:
        logging.debug("Unknown gsi version.")
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_UNKNOWN]

    if device_version == gsi_version:
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_TOT]
    else:
        return value | Status.TEST_TYPE_DICT[Status.TEST_TYPE_OTA]


class ScheduleHandler(webapp2.RequestHandler):
    """Background worker class for /worker/schedule_handler.

    This class pull tasks from 'queue-schedule' queue and processes in
    background service 'worker'.

    Attributes:
        logger: Logger class
    """
    logger = logger.Logger()

    def ReserveDevices(self, target_device_serials):
        """Reserves devices.

        Args:
            target_device_serials: a list of strings, containing target device
                                   serial numbers.
        """
        device_query = model.DeviceModel.query(
            model.DeviceModel.serial.IN(target_device_serials))
        devices = device_query.fetch()
        for device in devices:
            device.scheduling_status = Status.DEVICE_SCHEDULING_STATUS_DICT[
                "reserved"]
            device.put()

    def FindBuildId(self, artifact_type, manifest_branch, target,
                    signed=False):
        """Finds a designated build ID.

        Args:
            artifact_type: a string, build artifact type.
            manifest_branch: a string, build manifest branch.
            target: a string which build target and type are joined by '-'.
            signed: a boolean to get a signed build.

        Return:
            string, build ID found.
        """
        build_id = ""
        if "-" in target:
            build_target, build_type = target.split("-")
        else:
            build_target = target
            build_type = ""
        if not artifact_type or not manifest_branch or not build_target:
            self.logger.Println("The argument format is invalid.")
            return build_id
        build_query = model.BuildModel.query(
            model.BuildModel.artifact_type == artifact_type,
            model.BuildModel.manifest_branch == manifest_branch,
            model.BuildModel.build_target == build_target,
            model.BuildModel.build_type == build_type)
        builds = build_query.fetch()

        if builds:
            self.logger.Println("-- Found build ID")
            builds.sort(key=lambda x: x.build_id, reverse=True)
            for build in builds:
                if not signed or build.signed:
                    build_id = build.build_id
                    break
        return build_id

    def post(self):
        self.logger.Clear()
        schedule_query = model.ScheduleModel.query(
            model.ScheduleModel.suspended != True)
        schedules = schedule_query.fetch()

        if schedules:
            for schedule in schedules:
                self.logger.Println("")
                self.logger.Println("Schedule: %s (branch: %s)" %
                                    (schedule.test_name,
                                     schedule.manifest_branch))
                self.logger.Println("Build Target: %s" % schedule.build_target)
                self.logger.Println("Device: %s" % schedule.device)
                self.logger.Indent()
                if not self.NewPeriod(schedule):
                    self.logger.Println("- Skipped")
                    self.logger.Unindent()
                    continue

                target_host, target_device, target_device_serials = (
                    self.SelectTargetLab(schedule))
                if not target_host:
                    self.logger.Unindent()
                    continue

                self.logger.Println("- Target host: %s" % target_host)
                self.logger.Println("- Target device: %s" % target_device)
                self.logger.Println(
                    "- Target serials: %s" % target_device_serials)

                # create job and add.
                new_job = model.JobModel()
                new_job.hostname = target_host
                new_job.priority = schedule.priority
                new_job.test_name = schedule.test_name
                new_job.require_signed_device_build = (
                    schedule.require_signed_device_build)
                new_job.device = target_device
                new_job.period = schedule.period
                new_job.serial.extend(target_device_serials)
                new_job.build_storage_type = schedule.build_storage_type
                new_job.manifest_branch = schedule.manifest_branch
                new_job.build_target = schedule.build_target
                new_job.pab_account_id = schedule.device_pab_account_id
                new_job.shards = schedule.shards
                new_job.param = schedule.param
                new_job.retry_count = schedule.retry_count
                new_job.gsi_storage_type = schedule.gsi_storage_type
                new_job.gsi_branch = schedule.gsi_branch
                new_job.gsi_build_target = schedule.gsi_build_target
                new_job.gsi_pab_account_id = schedule.gsi_pab_account_id
                new_job.gsi_vendor_version = schedule.gsi_vendor_version
                new_job.test_storage_type = schedule.test_storage_type
                new_job.test_branch = schedule.test_branch
                new_job.test_build_target = schedule.test_build_target
                new_job.test_pab_account_id = schedule.test_pab_account_id
                new_job.parent_schedule = schedule.key

                # uses bit 0-1 to indicate version.
                test_type = GetTestVersionType(schedule.manifest_branch,
                                               schedule.gsi_branch)
                # uses bit 2
                if schedule.require_signed_device_build:
                    test_type |= Status.TEST_TYPE_DICT[Status.TEST_TYPE_SIGNED]
                new_job.test_type = test_type

                new_job.build_id = ""
                new_job.gsi_build_id = ""
                new_job.test_build_id = ""
                for artifact_type in ["device", "gsi", "test"]:
                    if artifact_type == "device":
                        storage_type_text = "build_storage_type"
                        manifest_branch_text = "manifest_branch"
                        build_target_text = "build_target"
                        build_id_text = "build_id"
                        signed = new_job.require_signed_device_build
                    else:
                        storage_type_text = artifact_type + "_storage_type"
                        manifest_branch_text = artifact_type + "_branch"
                        build_target_text = artifact_type + "_build_target"
                        build_id_text = artifact_type + "_build_id"
                        signed = False

                    manifest_branch = getattr(new_job, manifest_branch_text)
                    build_target = getattr(new_job, build_target_text)
                    storage_type = getattr(new_job, storage_type_text)
                    if storage_type == Status.STORAGE_TYPE_DICT["PAB"]:
                        build_id = self.FindBuildId(
                            artifact_type=artifact_type,
                            manifest_branch=manifest_branch,
                            target=build_target,
                            signed=signed)
                    elif storage_type == Status.STORAGE_TYPE_DICT["GCS"]:
                        # temp value to distinguish from empty values.
                        build_id = "gcs"
                    else:
                        build_id = ""
                        self.logger.Println(
                            "Unexpected storage type (%s)." % storage_type)
                    setattr(new_job, build_id_text, build_id)

                if (new_job.build_id and new_job.gsi_build_id
                        and new_job.test_build_id):
                    new_job.build_id = new_job.build_id.replace("gcs", "")
                    new_job.gsi_build_id = (new_job.gsi_build_id.replace(
                        "gcs", ""))
                    new_job.test_build_id = (new_job.test_build_id.replace(
                        "gcs", ""))
                    self.ReserveDevices(target_device_serials)
                    new_job.status = Status.JOB_STATUS_DICT["ready"]
                    new_job.timestamp = datetime.datetime.now()
                    new_job_key = new_job.put()
                    schedule.children_jobs.append(new_job_key)
                    schedule.put()
                    self.logger.Println("A new job has been created.")

                self.logger.Unindent()

        self.logger.Println("Scheduling completed.")

        lines = self.logger.Get()
        lines = [line.strip() for line in lines]
        outputs = []
        chars = 0
        for line in lines:
            chars += len(line)
            if chars > MAX_LOG_CHARACTERS:
                logging.info("\n".join(outputs))
                outputs = []
                chars = len(line)
            outputs.append(line)
        logging.info("\n".join(outputs))

    def NewPeriod(self, schedule):
        """Checks whether a new job creation is needed.

        Args:
            schedule: a proto containing schedule information.

        Returns:
            True if new job is required, False otherwise.
        """
        job_query = model.JobModel.query(
            model.JobModel.manifest_branch == schedule.manifest_branch,
            model.JobModel.build_target == schedule.build_target,
            model.JobModel.test_name == schedule.test_name,
            model.JobModel.period == schedule.period,
            model.JobModel.shards == schedule.shards,
            model.JobModel.retry_count == schedule.retry_count,
            model.JobModel.gsi_branch == schedule.gsi_branch,
            model.JobModel.test_branch == schedule.test_branch)
        same_jobs = job_query.fetch()
        same_jobs = [
            x for x in same_jobs
            if (set(x.param) == set(schedule.param)
                and x.device in schedule.device)
        ]
        if not same_jobs:
            return True

        outdated_jobs = [
            x for x in same_jobs
            if (datetime.datetime.now() - x.timestamp > datetime.timedelta(
                minutes=x.period))
        ]
        outdated_ready_jobs = [
            x for x in outdated_jobs
            if x.status == Status.JOB_STATUS_DICT["expired"]
        ]

        if outdated_ready_jobs:
            self.logger.Println(
                ("Job key[{}] is(are) outdated. "
                 "They became infra-err status.").format(
                     ", ".join(
                         [str(x.key.id()) for x in outdated_ready_jobs])))
            for job in outdated_ready_jobs:
                job.status = Status.JOB_STATUS_DICT["infra-err"]
                job.put()
                model_util.UpdateParentSchedule(job, job.status)

        outdated_leased_jobs = [
            x for x in outdated_jobs
            if x.status == Status.JOB_STATUS_DICT["leased"]
        ]
        if outdated_leased_jobs:
            self.logger.Println(
                ("Job key[{}] is(are) expected to be completed "
                 "however still in leased status.").format(
                     ", ".join(
                         [str(x.key.id()) for x in outdated_leased_jobs])))

        recent_jobs = [x for x in same_jobs if x not in outdated_jobs]

        if recent_jobs or outdated_leased_jobs:
            return False
        else:
            return True

    def SelectTargetLab(self, schedule):
        """Find target host and devices to schedule a new job.

        Args:
            schedule: a proto containing the information of a schedule.

        Returns:
            a string which represents hostname,
            a string containing target lab and product with '/' separator,
            a list of selected devices serial (see whether devices will be
            selected later when the job is picked up.)
        """
        for target_device in schedule.device:
            if "/" not in target_device:
                # device malformed
                continue

            target_lab, target_product_type = target_device.split("/")
            self.logger.Println("- Lab %s" % target_lab)
            self.logger.Indent()
            lab_query = model.LabModel.query(model.LabModel.name == target_lab)
            target_labs = lab_query.fetch()

            available_devices = {}
            if target_labs:
                for lab in target_labs:
                    self.logger.Println("- Host: %s" % lab.hostname)
                    self.logger.Indent()
                    device_query = model.DeviceModel.query(
                        model.DeviceModel.hostname == lab.hostname)
                    host_devices = device_query.fetch()

                    for device in host_devices:
                        if ((device.status in [
                                Status.DEVICE_STATUS_DICT["fastboot"],
                                Status.DEVICE_STATUS_DICT["online"],
                                Status.DEVICE_STATUS_DICT["ready"]
                        ]) and (device.scheduling_status ==
                                Status.DEVICE_SCHEDULING_STATUS_DICT["free"])
                                and device.product.lower() ==
                                target_product_type.lower()):
                            self.logger.Println("- Found %s %s %s" %
                                                (device.product, device.status,
                                                 device.serial))
                            if device.hostname not in available_devices:
                                available_devices[device.hostname] = set()
                            available_devices[device.hostname].add(
                                device.serial)
                    self.logger.Unindent()
                for host in available_devices:
                    if len(available_devices[host]) >= schedule.shards:
                        self.logger.Println("All devices found.")
                        self.logger.Unindent()
                        return host, target_device, list(
                            available_devices[host])[:schedule.shards]
                self.logger.Println(
                    "- Not enough devices found, while %s required.\n%s" %
                    (schedule.shards, available_devices))
            self.logger.Unindent()
        return None, None, []
