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
import { HttpClient, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { catchError } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { DeviceWrapper } from '../../model/device_wrapper';
import { ServiceBase } from '../../shared/servicebase';


@Injectable()
export class DeviceService extends ServiceBase {
  constructor(public httpClient: HttpClient) {
    super(httpClient);
    this.url = environment['baseURL'] + '/host_info/v1/';
  }

  getDevices(size: number,
             offset: number,
             filterInfo: string,
             sort: string,
             direction: string): Observable<HttpResponse<DeviceWrapper>> {
    const url = this.url + 'get';
    return this.httpClient.get<DeviceWrapper>(url,  {observe: 'response', params: new HttpParams()
        .append('size', String(size))
        .append('offset', String(offset))
        .append('filter', filterInfo)
        .append('sort', sort)
        .append('direction', direction)})
      .pipe(catchError(this.handleError));
  }
}
