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
import { Component, OnInit } from '@angular/core';
import { MatTableDataSource, PageEvent } from '@angular/material';

import { Device } from '../../model/device';
import { DeviceService } from './device.service';
import { MenuBaseClass } from '../menu_base';

/** Component that handles device menu. */
@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  providers: [ DeviceService ],
  styleUrls: ['./device.component.scss'],
})
export class DeviceComponent extends MenuBaseClass implements OnInit {
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

  ngOnInit(): void {
    this.getCount();
    this.getDevices(this.pageSize, this.pageSize * this.pageIndex);
  }

  /** Gets a total count of devices. */
  getCount(observer = this.getDefaultCountObservable()) {
    const filterJSON = '';
    this.deviceService.getCount(filterJSON).subscribe(observer);
  }

  /** Gets devices.
   * @param size A number, at most this many results will be returned.
   * @param offset A Number of results to skip.
   */
  getDevices(size = 0, offset = 0) {
    this.loading = true;
    const filterJSON = '';
    this.deviceService.getDevices(size, offset, filterJSON, '', '')
      .subscribe(
        (response) => {
          this.loading = false;
          if (this.count >= 0) {
            let length = 0;
            if (response.body.devices) {
              length = response.body.devices.length;
            }
            const total = length + offset;
            if (response.body.has_next) {
              if (length !== this.pageSize) {
                console.log('Received unexpected number of entities.');
              } else if (this.count <= total) {
                this.getCount();
              }
            } else {
              if (this.count !== total) {
                if (length !== this.count) {
                  this.getCount();
                } else if (this.count > total) {
                  const countObservable = this.getDefaultCountObservable([
                    () => {
                      this.pageIndex = Math.floor(this.count / this.pageSize);
                      this.getDevices(this.pageSize, this.pageSize * this.pageIndex);
                    }
                  ]);
                  this.getCount(countObservable);
                }
              }
            }
          }
          this.dataSource.data = response.body.devices;
        },
        (error) => console.log(`[${error.status}] ${error.name}`)
      );
  }

  /** Hooks a page event and handles properly. */
  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.getDevices(this.pageSize, this.pageSize * this.pageIndex);
    return event;
  }
}
