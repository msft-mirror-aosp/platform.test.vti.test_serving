import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'

import {BuildRoutingModule} from './build-routing.module';
import {SharedModule} from '../shared/modules/shared.module';

import {BuildListComponent} from './build-list/build-list.component';
import {BuildTopComponent} from './build-top/build-top.component';
import {BuildService} from './shared/build.service';
import {BuildComponent} from './build.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    BuildRoutingModule,
    ReactiveFormsModule
  ],
  declarations: [
    BuildComponent,
    BuildListComponent,
    BuildTopComponent
  ],
  entryComponents: [
  ],
  providers: [
    BuildService
  ]
})

export class BuildModule {
}
