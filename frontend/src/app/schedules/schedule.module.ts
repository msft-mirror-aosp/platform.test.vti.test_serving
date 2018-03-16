import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'

import {ScheduleRoutingModule} from './schedule-routing.module';
import {SharedModule} from '../shared/modules/shared.module';

import {ScheduleListComponent} from './schedule-list/schedule-list.component';
import {ScheduleTopComponent} from './schedule-top/schedule-top.component';
import {ScheduleService} from './shared/schedule.service';
import {ScheduleComponent} from './schedule.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    ScheduleRoutingModule,
    ReactiveFormsModule
  ],
  declarations: [
    ScheduleComponent,
    ScheduleListComponent,
    ScheduleTopComponent
  ],
  entryComponents: [
  ],
  providers: [
    ScheduleService
  ]
})

export class ScheduleModule {
}
