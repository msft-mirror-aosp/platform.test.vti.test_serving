import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {DeviceListComponent} from './device-list/device-list.component';
import {DeviceComponent} from './device.component';

const devicesRoutes: Routes = [
  {
    path: '',
    component: DeviceComponent,
    children: [
      {path: '', component: DeviceListComponent},
      // {path: ':id', component: HeroDetailComponent}
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(devicesRoutes)
  ],
  exports: [
    RouterModule
  ]
})

export class DeviceRoutingModule {
}
