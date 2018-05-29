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


class DeviceStats(object):
  """Device stats class.

  Attributes:
      _total: int, total device count.
      _active: int, device count in active state.
      _error: int, device count in error state.
      _idle: int, device count in ready state.
  """

  def __init__(self, parent=True):
    self._total = 0
    self._active = 0
    self._error = 0
    self._idle = 0
    if parent == True:
      self._product_stat = {}

  @property
  def total(self):
    return self._total

  @total.setter
  def total(self, total):
    self._total = total

  @property
  def active(self):
    return self._active

  @active.setter
  def active(self, active):
    self._active = active

  @property
  def error(self):
    return self._error

  @error.setter
  def error(self, error):
    self._error = error

  @property
  def idle(self):
    return self._idle

  @idle.setter
  def idle(self, idle):
    self._idle = idle

  @property
  def utilization(self):
    return self._active * 100 / self._total

  @property
  def error_ratio(self):
    return self._error * 100 / self._total

  @property
  def product_stat(self):
    return self._product_stat

  def __getitem__(self, product):
    return self._product_stat[product]

  def _add_total(self, product=""):
    self._total += 1
    if product:
      if product not in self._product_stat:
        self._product_stat[product] = DeviceStats(False)
      self._product_stat[product].total += 1

  def add_active(self, product=""):
    self._add_total(product)
    self._active += 1
    if product:
      self._product_stat[product].active += 1

  def add_error(self, product=""):
    self._add_total(product)
    self._error += 1
    if product:
      self._product_stat[product].error += 1

  def add_idle(self, product=""):
    self._add_total(product)
    self._idle += 1
    if product:
      self._product_stat[product].idle += 1