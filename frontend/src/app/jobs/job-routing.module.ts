import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {JobListComponent} from './job-list/job-list.component';
import {JobComponent} from './job.component';

const jobsRoutes: Routes = [
  {
    path: '',
    component: JobComponent,
    children: [
      {path: '', component: JobListComponent},
      // {path: ':id', component: HeroDetailComponent}
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(jobsRoutes)
  ],
  exports: [
    RouterModule
  ]
})

export class JobRoutingModule {
}
