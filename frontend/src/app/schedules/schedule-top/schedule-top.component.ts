import {Component} from '@angular/core';

import {Schedule} from '../shared/schedule.model';

import {ScheduleService} from '../shared/schedule.service';
import {AppConfig} from '../../config/app.config';

@Component({
  selector: 'app-schedule-top',
  templateUrl: './schedule-top.component.html',
  styleUrls: ['./schedule-top.component.scss']
})
export class ScheduleTopComponent {

  schedules: Schedule[] = null;
  canVote = false;

  constructor(private scheduleService: ScheduleService) {
    this.canVote = this.scheduleService.checkIfUserCanVote();

    this.scheduleService.getAllSchedules().subscribe((schedules) => {
      this.schedules = schedules.sort((a, b) => {
        return b.likes - a.likes;
      }).slice(0, AppConfig.topHeroesLimit);
    });
  }

  like(schedule: Schedule): Promise<any> {
    return new Promise((resolve, reject) => {
      this.scheduleService.like(schedule).subscribe(() => {
        this.canVote = this.scheduleService.checkIfUserCanVote();
        resolve(true);
      }, (error) => {
        reject(error);
      });
    });
  }
}
