import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {BuildListComponent} from './build-list/build-list.component';
import {BuildComponent} from './build.component';

const buildsRoutes: Routes = [
  {
    path: '',
    component: BuildComponent,
    children: [
      {path: '', component: BuildListComponent},
      // {path: ':id', component: HeroDetailComponent}
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(buildsRoutes)
  ],
  exports: [
    RouterModule
  ]
})

export class BuildRoutingModule {
}
