import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {ScheduleListComponent} from './schedule-list/schedule-list.component';
import {ScheduleComponent} from './schedule.component';

const schedulesRoutes: Routes = [
  {
    path: '',
    component: ScheduleComponent,
    children: [
      {path: '', component: ScheduleListComponent},
      // {path: ':id', component: HeroDetailComponent}
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(schedulesRoutes)
  ],
  exports: [
    RouterModule
  ]
})

export class ScheduleRoutingModule {
}
