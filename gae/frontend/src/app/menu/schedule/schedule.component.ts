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
import { MatSnackBar, MatTableDataSource, PageEvent } from '@angular/material';

import { MenuBaseClass } from '../menu_base';
import { Schedule } from '../../model/schedule';
import { ScheduleService } from './schedule.service';

/** Component that handles schedule menu. */
@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  providers: [ ScheduleService ],
  styleUrls: ['./schedule.component.scss'],
})
export class ScheduleComponent extends MenuBaseClass implements OnInit {
  columnTitles = [
    '_index',
    'test_name',
    'device',
    'manifest_branch',
    'build_target',
    'gsi_branch',
    'gsi_build_target',
    'test_branch',
    'test_build_target',
    'period',
    'timestamp',
  ];
  dataSource = new MatTableDataSource<Schedule>();
  pageEvent: PageEvent;

  constructor(private scheduleService: ScheduleService,
              public snackBar: MatSnackBar) {
    super(snackBar);
  }

  ngOnInit(): void {
    this.getCount();
    this.getSchedules(this.pageSize, this.pageSize * this.pageIndex);
  }

  /** Gets a total count of schedules. */
  getCount(observer = this.getDefaultCountObservable()) {
    const filterJSON = '';
    this.scheduleService.getCount(filterJSON).subscribe(observer);
  }

  /** Gets schedules.
   * @param size A number, at most this many results will be returned.
   * @param offset A Number of results to skip.
   */
  getSchedules(size = 0, offset = 0) {
    this.loading = true;
    const filterJSON = '';
    this.scheduleService.getSchedules(size, offset, filterJSON, '', '')
      .subscribe(
        (response) => {
          this.loading = false;
          if (this.count >= 0) {
            let length = 0;
            if (response.schedules) {
              length = response.schedules.length;
            }
            const total = length + offset;
            if (response.has_next) {
              if (length !== this.pageSize) {
                this.showSnackbar('Received unexpected number of entities.');
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
                      this.getSchedules(this.pageSize, this.pageSize * this.pageIndex);
                    }
                  ]);
                  this.getCount(countObservable);
                }
              }
            }
          }
          this.dataSource.data = response.schedules;
        },
        (error) => this.showSnackbar(`[${error.status}] ${error.name}`)
      );
  }

  /** Hooks a page event and handles properly. */
  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.getSchedules(this.pageSize, this.pageSize * this.pageIndex);
    return event;
  }
}
