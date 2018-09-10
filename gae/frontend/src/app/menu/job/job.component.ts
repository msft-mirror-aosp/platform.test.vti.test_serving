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

import { FilterCondition } from '../../model/filter_condition';
import { FilterItem } from '../../model/filter_item';
import { MenuBaseClass } from '../menu_base';
import { Job } from '../../model/job';
import { JobService } from './job.service';
import { JobStatus, TestType } from '../../shared/vtslab_status';

import * as moment from 'moment-timezone';

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
  statColumnTitles = [
    'hours',
    'created',
    'completed',
    'running',
    'bootup_err',
    'infra_err',
    'expired',
  ];
  dataSource = new MatTableDataSource<Job>();
  statDataSource = new MatTableDataSource();
  pageEvent: PageEvent;
  jobStatusEnum = JobStatus;

  constructor(private jobService: JobService) {
    super();
  }

  ngOnInit(): void {
    this.getCount();
    this.getStatistics();
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
            if (response.jobs) {
              length = response.jobs.length;
            }
            const total = length + offset;
            if (response.has_next) {
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
          this.dataSource.data = response.jobs;
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

  /** Gets the recent jobs and calculate statistics */
  getStatistics() {
    const timeFilter = new FilterItem();
    timeFilter.key = 'timestamp';
    timeFilter.method = FilterCondition.GreaterThan;
    timeFilter.value = '72';
    const timeFilterString = JSON.stringify([timeFilter]);
    this.jobService.getJobs(0, 0, timeFilterString, '', '')
      .subscribe(
        (response) => {
          const stats_72hrs = this.buildStatisticsData('72 Hours', response.jobs);
          const jobs_24hrs = (response.jobs == null || response.jobs.length === 0) ? undefined : response.jobs.filter(
            job => (moment() - moment.tz(job.timestamp, 'YYYY-MM-DDThh:mm:ss', 'UTC')) / 3600000 < 24);
          const stats_24hrs = this.buildStatisticsData('24 Hours', jobs_24hrs);
          this.statDataSource.data = [stats_24hrs, stats_72hrs];
        },
        (error) => console.log(`[${error.status}] ${error.name}`)
      );
  }

  /** Builds statistics from given jobs list */
  buildStatisticsData(title, jobs) {
    if (jobs == null || jobs.length === 0) {
      return { hours: title, created: 0, completed: 0, running: 0, bootup_err: 0, infra_err: 0, expired: 0 };
    }
    return {
      hours: title,
      created: jobs.length,
      completed: jobs.filter(job => job.status != null && Number(job.status) === JobStatus.Complete).length,
      running: jobs.filter(job => job.status != null &&
        (Number(job.status) === JobStatus.Leased || Number(job.status) === JobStatus.Ready)).length,
      bootup_err: jobs.filter(job => job.status != null && Number(job.status) === JobStatus.Bootup_err).length,
      infra_err: jobs.filter(job => job.status != null && Number(job.status) === JobStatus.Infra_err).length,
      expired: jobs.filter(job => job.status != null && Number(job.status) === JobStatus.Expired).length,
    };
  }

  /** Generates text to represent in HTML with given test type. */
  getTestTypeText(status: number) {
    if (status === undefined || status & TestType.Unknown) {
      return TestType[TestType.Unknown];
    }

    const text_list = [];
    [TestType.ToT, TestType.OTA, TestType.Signed, TestType.Manual].forEach(function (value) {
      if (status & value) { text_list.push(TestType[value]); }
    });

    return text_list.join(', ');
  }
}
