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

import { MenuBaseClass } from '../menu_base';
import { Schedule } from '../../model/schedule';
import { ScheduleService } from './schedule.service';


@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  providers: [ ScheduleService ],
  styleUrls: ['./schedule.component.scss'],
})
export class ScheduleComponent extends MenuBaseClass {
  columnTitles = [
    '_index',
    'build_target',
    'device',
    'gsi_branch',
    'gsi_build_target',
    'manifest_branch',
    'period',
    'test_branch',
    'test_build_target',
    'test_name',
    'timestamp',
  ];
  dataSource = new MatTableDataSource<Schedule>();
  pageEvent: PageEvent;

  constructor(private scheduleService: ScheduleService) {
    super();
  }

  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    return event;
  }
}
