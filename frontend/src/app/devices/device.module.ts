import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'

import {DeviceRoutingModule} from './device-routing.module';
import {SharedModule} from '../shared/modules/shared.module';

import {DeviceListComponent} from './device-list/device-list.component';
import {DeviceTopComponent} from './device-top/device-top.component';
import {DeviceService} from './shared/device.service';
import {DeviceComponent} from './device.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    DeviceRoutingModule,
    ReactiveFormsModule
  ],
  declarations: [
    DeviceComponent,
    DeviceListComponent,
    DeviceTopComponent
  ],
  entryComponents: [
  ],
  providers: [
    DeviceService
  ]
})

export class DeviceModule {
}
