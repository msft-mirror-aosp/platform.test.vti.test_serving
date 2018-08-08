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
import { MatTableDataSource } from '@angular/material';

import { Host } from '../../model/host';
import { Lab } from '../../model/lab';
import { LabService } from './lab.service';
import { MenuBaseClass } from '../menu_base';


@Component({
  selector: 'app-lab',
  templateUrl: './lab.component.html',
  providers: [ LabService ],
  styleUrls: ['./lab.component.scss'],
})
export class LabComponent extends MenuBaseClass {
  labColumnTitles = [
    '_index',
    'admin',
    'hostCount',
    'name',
    'owner',
  ];
  hostColumnTitles = [
    '_index',
    'host_equipment',
    'hostname',
    'ip',
    'name',
    'vtslab_version',
  ];
  labCount = -1;

  constructor(private labService: LabService) {
    super();
  }

  labDataSource = new MatTableDataSource<Lab>();
  hostDataSource = new MatTableDataSource<Host>();
}
