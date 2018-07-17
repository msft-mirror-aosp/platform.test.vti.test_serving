# Copyright 2018 Google Inc. All rights reserved.
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

import logging
import inspect

from protorpc import messages
from protorpc import remote
from google.appengine.ext import ndb


class EndpointBase(remote.Service):
    """A base class for endpoint implementation."""

    def GetCommonAttributes(self, resource, reference):
        """Gets a list of common attribute names.

        This method finds the attributes assigned in 'resource' instance, and
        filters out if the attributes are not a member of 'reference' class.

        Args:
            resource: either a protorpc.messages.Message instance,
                      or a ndb.Model instance.
            reference: either a protorpc.messages.Message class,
                       or a ndb.Model class.

        Returns:
            a list of string, attribute names exist on resource and reference.

        Raises:
            ValueError if resource or reference is not supported class.
        """
        # check resource type and absorb list of assigned attributes.
        resource_attrs = self.GetAttributes(resource, assigned_only=True)
        reference_attrs = self.GetAttributes(reference)
        return [x for x in resource_attrs if x in reference_attrs]

    def GetAttributes(self, value, assigned_only=False):
        """Gets a list of attributes.

        Args:
            value: a class instance or a class itself.
            assigned_only: True to get only assigned attributes when value is
                           an instance, False to get all attributes.

        Raises:
            ValueError if value is not supported class.
        """
        attrs = []
        if inspect.isclass(value):
            if assigned_only:
                logging.warning(
                    "Please use a class instance for 'resource' argument.")

            if (issubclass(value, messages.Message)
                    or issubclass(value, ndb.Model)):
                attrs = [
                    x[0] for x in value.__dict__.items()
                    if not x[0].startswith("_")
                ]
            else:
                raise ValueError("Only protorpc.messages.Message or ndb.Model "
                                 "class are supported.")
        else:
            if isinstance(value, messages.Message):
                attrs = [
                    x.name for x in value.all_fields()
                    if not assigned_only or value.get_assigned_value(x.name)
                ]
            elif isinstance(value, ndb.Model):
                attrs = [
                    x for x in list(value.to_dict())
                    if not assigned_only or getattr(value, x, None)
                ]
            else:
                raise ValueError("Only protorpc.messages.Message or ndb.Model "
                                 "class are supported.")

        return attrs
