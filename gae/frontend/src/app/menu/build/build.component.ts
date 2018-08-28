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

import { Build } from '../../model/build';
import { BuildService } from './build.service';
import { MenuBaseClass } from '../menu_base';

/** Component that handles build menu. */
@Component({
  selector: 'app-build',
  templateUrl: './build.component.html',
  providers: [ BuildService ],
  styleUrls: ['./build.component.scss'],
})
export class BuildComponent extends MenuBaseClass implements OnInit {
  columnTitles = [
    '_index',
    'artifact_type',
    'build_id',
    'build_target',
    'build_type',
    'manifest_branch',
    'signed'];
  dataSource = new MatTableDataSource<Build>();
  pageEvent: PageEvent;

  constructor(private buildService: BuildService) {
    super();
  }

  ngOnInit(): void {
    this.getCount();
    this.getBuilds(this.pageSize, this.pageSize * this.pageIndex);
  }

  /** Gets a total count of builds. */
  getCount(observer = this.getDefaultCountObservable()) {
    const filterJSON = '';
    this.buildService.getCount(filterJSON).subscribe(observer);
  }

  /** Gets builds.
   * @param size A number, at most this many results will be returned.
   * @param offset A Number of results to skip.
   */
  getBuilds(size = 0, offset = 0) {
    this.loading = true;
    const filterJSON = '';
    this.buildService.getBuilds(size, offset, filterJSON, '', '')
      .subscribe(
        (response) => {
          this.loading = false;
          if (this.count >= 0) {
            let length = 0;
            if (response.body.builds) {
              length = response.body.builds.length;
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
                      this.getBuilds(this.pageSize, this.pageSize * this.pageIndex);
                    }
                  ]);
                  this.getCount(countObservable);
                }
              }
            }
          }
          this.dataSource.data = response.body.builds;
        },
        (error) => console.log(`[${error.status}] ${error.name}`)
      );
  }

  /** Hooks a page event and handles properly. */
  onPageEvent(event: PageEvent) {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.getBuilds(this.pageSize, this.pageSize * this.pageIndex);
    return event;
  }
}
