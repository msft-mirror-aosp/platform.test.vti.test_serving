import {Component} from '@angular/core';

import {Job} from '../shared/job.model';

import {JobService} from '../shared/job.service';
import {AppConfig} from '../../config/app.config';

@Component({
  selector: 'app-hero-top',
  templateUrl: './job-top.component.html',
  styleUrls: ['./job-top.component.scss']
})
export class JobTopComponent {

  jobs: Job[] = null;
  canVote = false;

  constructor(private jobService: JobService) {
    this.canVote = this.jobService.checkIfUserCanVote();

    this.jobService.getAllJobs().subscribe((jobs) => {
      this.jobs = jobs.sort((a, b) => {
        return b.likes - a.likes;
      }).slice(0, AppConfig.topHeroesLimit);
    });
  }

  like(job: Job): Promise<any> {
    return new Promise((resolve, reject) => {
      this.jobService.like(job).subscribe(() => {
        this.canVote = this.jobService.checkIfUserCanVote();
        resolve(true);
      }, (error) => {
        reject(error);
      });
    });
  }
}
