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

import logging
import re

from google.appengine.api import app_identity
from google.appengine.api import mail

SENDER_ADDRESS = "noreply@{}.appspotmail.com".format(
    app_identity.get_application_id())

SEND_DEVICE_NOTIFICATION_HEADER = "Devices in lab {} are not responding."
SEND_DEVICE_NOTIFICATION_FOOTER = ("You are receiving this email because "
                                   "you are listed as an owner, or an "
                                   "administrator, to the lab {}.\n"
                                   "If you received this email by mistake, "
                                   "please send an email to "
                                   "vtslab-dev@google.com. Thank you.")


def send_device_notification(devices):
    """Sends notification for not responding devices.

    Args:
        devices: a dict containing lab and host information of no-response
                 devices.
    """
    for lab in devices:
        email_message = mail.EmailMessage()
        email_message.sender = SENDER_ADDRESS
        try:
            email_message.to = verify_recipient_address(
                devices[lab]["_recipients"])
        except ValueError as e:
            logging.error(e)
            continue
        email_message.subject = (
            "[VTS lab] Devices not responding in lab {}".format(lab))
        message = ""
        message += SEND_DEVICE_NOTIFICATION_HEADER.format(lab)
        message += "\n\n"
        for host in devices[lab]:
            if host == "_recipients" or not devices[lab][host]:
                continue
            message += "hostname\n"
            message += host
            message += "\n\ndevices\n"
            message += "\n".join(devices[lab][host])
            message += "\n\n\n"
        message += "\n\n"
        message += SEND_DEVICE_NOTIFICATION_FOOTER.format(lab)

        try:
            email_message.body = message
            email_message.check_initialized()
            email_message.send()
        except mail.MissingRecipientError as e:
            logging.exception(e)


def verify_recipient_address(address):
    """Verifies recipients address.

    Args:
        address: a list of strings or a string, recipient(s) address.

    Returns:
        A list of verified addresses if list type argument is given, or
        a string of a verified address if str type argument is given.

    Raises:
        ValueError if type of address is neither list nor str.
    """
    # pattern for 'any@google.com', and 'any name <any@google.com>'
    verify_patterns = [
        re.compile(".*@google\.com$"),
        re.compile(".*<.*@google\.com>$")
    ]
    if not address:
        return None
    if type(address) is list:
        verified_address = [
            x for x in address
            if any(pattern.match(x) for pattern in verify_patterns)
        ]
        return verified_address
    elif type(address) is str:
        return address if any(
            pattern.match(address) for pattern in verify_patterns) else None
    else:
        raise ValueError("Wrong type - {}.".format(type(address)))
