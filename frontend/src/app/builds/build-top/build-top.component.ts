import {Component} from '@angular/core';

import {Build} from '../shared/build.model';

import {BuildService} from '../shared/build.service';
import {AppConfig} from '../../config/app.config';

@Component({
  selector: 'app-build-top',
  templateUrl: './build-top.component.html',
  styleUrls: ['./build-top.component.scss']
})
export class BuildTopComponent {

  builds: Build[] = null;
  canVote = false;

  constructor(private buildService: BuildService) {
    this.canVote = this.buildService.checkIfUserCanVote();

    this.buildService.getAllBuilds().subscribe((builds) => {
      this.builds = builds.sort((a, b) => {
        return b.likes - a.likes;
      }).slice(0, AppConfig.topHeroesLimit);
    });
  }

  like(build: Build): Promise<any> {
    return new Promise((resolve, reject) => {
      this.buildService.like(build).subscribe(() => {
        this.canVote = this.buildService.checkIfUserCanVote();
        resolve(true);
      }, (error) => {
        reject(error);
      });
    });
  }
}
