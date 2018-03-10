import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'

import {JobRoutingModule} from './job-routing.module';
import {SharedModule} from '../shared/modules/shared.module';

import {JobListComponent, RemoveJobDialogComponent} from './job-list/job-list.component';
import {JobTopComponent} from './job-top/job-top.component';
import {JobService} from './shared/job.service';
import {JobComponent} from './job.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    JobRoutingModule,
    ReactiveFormsModule
  ],
  declarations: [
    JobComponent,
    JobListComponent,
    JobTopComponent,
    RemoveJobDialogComponent
  ],
  entryComponents: [
    RemoveJobDialogComponent
  ],
  providers: [
    JobService
  ]
})

export class JobModule {
}
