import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

import {AppConfig} from '../../config/app.config';

import {Build} from './build.model';
import {Observable} from 'rxjs/Observable';
import {MatSnackBar, MatSnackBarConfig} from '@angular/material';
import {TranslateService} from '@ngx-translate/core';

@Injectable()
export class BuildService {
  private headers: HttpHeaders;
  private buildUrl: string;
  private translations: any;

  private handleError(error: any) {
    if (error instanceof Response) {
      return Observable.throw(error.json()['error'] || 'backend server error');
    }
    return Observable.throw(error || 'backend server error');
  }

  constructor(private http: HttpClient,
              private translateService: TranslateService,
              private snackBar: MatSnackBar) {
    this.buildUrl = AppConfig.endpoints.heroes;
    this.headers = new HttpHeaders({'Content-Type': 'application/json'});

    this.translateService.get(['heroCreated', 'saved', 'heroLikeMaximum', 'heroRemoved'], {
      'value': AppConfig.votesLimit
    }).subscribe((texts) => {
      this.translations = texts;
    });
  }

  getAllBuilds(): Observable<Build[]> {
    return this.http.get(this.buildUrl)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  getBuildById(buildId: string): Observable<Build> {
    return this.http.get(this.buildUrl + '/' + buildId)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  createBuild(build: any): Observable<Build> {
    return this.http
      .post(this.buildUrl, JSON.stringify({
        name: build.name,
        alterEgo: build.alterEgo
      }), {headers: this.headers})
      .map(response => {
        this.showSnackBar('heroCreated');
        return response;
      })
      .catch(error => this.handleError(error));
  }

  like(build: Build) {
    if (this.checkIfUserCanVote()) {
      const url = `${this.buildUrl}/${build.id}/like`;
      return this.http
        .post(url, {}, {headers: this.headers})
        .map((response) => {
          localStorage.setItem('votes', '' + (Number(localStorage.getItem('votes')) + 1));
          build.likes += 1;
          this.showSnackBar('saved');
          return response;
        })
        .catch(error => this.handleError(error));
    } else {
      this.showSnackBar('heroLikeMaximum');
      return Observable.throw('maximum votes');
    }
  }

  checkIfUserCanVote(): boolean {
    return Number(localStorage.getItem('votes')) < AppConfig.votesLimit;
  }

  deleteBuildById(id: any): Observable<Array<Build>> {
    const url = `${this.buildUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .map((response) => {
        this.showSnackBar('buildRemoved');
        return response;
      })
      .catch(error => this.handleError(error));
  }

  showSnackBar(name): void {
    const config: any = new MatSnackBarConfig();
    config.duration = AppConfig.snackBarDuration;
    this.snackBar.open(this.translations[name], 'OK', config);
  }
}
