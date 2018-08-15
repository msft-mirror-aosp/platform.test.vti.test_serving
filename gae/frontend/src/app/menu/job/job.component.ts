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
import { Job } from '../../model/job';
import { JobService } from './job.service';


@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  providers: [ JobService ],
  styleUrls: ['./job.component.scss'],
})
export class JobComponent extends MenuBaseClass {
  columnTitles = [
    '_index',
    'build_id',
    'build_target',
    'device',
    'gsi_branch',
    'gsi_build_id',
    'gsi_build_target',
    'heartbeat_stamp',
    'hostname',
    'manifest_branch',
    'serial',
    'status',
    'test_branch',
    'test_build_id',
    'test_build_target',
    'test_name',
    'test_type',
    'timestamp',
  ];
  dataSource = new MatTableDataSource<Job>();
  pageEvent: PageEvent;

  constructor(private jobService: JobService) {
    super();
  }

  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    return event;
  }
}
