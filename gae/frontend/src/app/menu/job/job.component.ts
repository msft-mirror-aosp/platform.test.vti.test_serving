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

import { MenuBaseClass } from '../menu_base';
import { Job } from '../../model/job';
import { JobService } from './job.service';

/** Component that handles job menu. */
@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  providers: [ JobService ],
  styleUrls: ['./job.component.scss'],
})
export class JobComponent extends MenuBaseClass implements OnInit {
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

  ngOnInit(): void {
    this.getCount();
    this.getJobs(this.pageSize, this.pageSize * this.pageIndex);
  }

  /** Gets a total count of jobs. */
  getCount(observer = this.getDefaultCountObservable()) {
    const filterJSON = '';
    this.jobService.getCount(filterJSON).subscribe(observer);
  }

  /** Gets jobs.
   * @param size A number, at most this many results will be returned.
   * @param offset A Number of results to skip.
   */
  getJobs(size = 0, offset = 0) {
    this.loading = true;
    const filterJSON = '';
    this.jobService.getJobs(size, offset, filterJSON, '', '')
      .subscribe(
        (response) => {
          this.loading = false;
          if (this.count >= 0) {
            let length = 0;
            if (response.body.jobs) {
              length = response.body.jobs.length;
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
                      this.getJobs(this.pageSize, this.pageSize * this.pageIndex);
                    }
                  ]);
                  this.getCount(countObservable);
                }
              }
            }
          }
          this.dataSource.data = response.body.jobs;
        },
        (error) => console.log(`[${error.status}] ${error.name}`)
      );
  }

  /** Hooks a page event and handles properly. */
  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.getJobs(this.pageSize, this.pageSize * this.pageIndex);
    return event;
  }
}
