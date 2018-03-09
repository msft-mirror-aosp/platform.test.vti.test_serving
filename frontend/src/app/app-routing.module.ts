import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

// import {HeroTopComponent} from './heroes/hero-top/hero-top.component';
import {AppConfig} from './config/app.config';
import {Error404Component} from './core/error/404/404.component';

const routes: Routes = [
  {path: '', redirectTo: '/', pathMatch: 'full'},
  // {path: '', component: HeroTopComponent},
  {path: AppConfig.routes.builds, loadChildren: 'app/builds/build.module#BuildModule'},
  {path: AppConfig.routes.jobs, loadChildren: 'app/jobs/job.module#JobModule'},
  {path: AppConfig.routes.devices, loadChildren: 'app/devices/device.module#DeviceModule'},
  {path: AppConfig.routes.schedules, loadChildren: 'app/schedules/schedule.module#ScheduleModule'},
  {path: AppConfig.routes.error404, component: Error404Component},

  // otherwise redirect to 404
  {path: '**', redirectTo: '/' + AppConfig.routes.error404}
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})

export class AppRoutingModule {
}