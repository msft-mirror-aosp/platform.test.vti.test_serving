/**
 * Copyright (C) 2018 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { Component } from '@angular/core';
import { MatTableDataSource, PageEvent } from '@angular/material';

import { Device } from '../../model/device';
import { DeviceService } from './device.service';
import { MenuBaseClass } from '../menu_base';


@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  providers: [ DeviceService ],
  styleUrls: ['./device.component.scss'],
})
export class DeviceComponent extends MenuBaseClass {
  columnTitles = [
    '_index',
    'device_equipment',
    'hostname',
    'product',
    'scheduling_status',
    'serial',
    'status',
  ];
  dataSource = new MatTableDataSource<Device>();
  pageEvent: PageEvent;

  constructor(private deviceService: DeviceService) {
    super();
  }

  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    return event;
  }
}
