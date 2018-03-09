import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

import {AppConfig} from '../../config/app.config';

import {Schedule} from './schedule.model';
import {Observable} from 'rxjs/Observable';
import {MatSnackBar, MatSnackBarConfig} from '@angular/material';
import {TranslateService} from '@ngx-translate/core';

@Injectable()
export class ScheduleService {
  private headers: HttpHeaders;
  private heroesUrl: string;
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
    this.heroesUrl = AppConfig.endpoints.heroes;
    this.headers = new HttpHeaders({'Content-Type': 'application/json'});

    this.translateService.get(['scheduleCreated', 'saved', 'heroLikeMaximum', 'heroRemoved'], {
      'value': AppConfig.votesLimit
    }).subscribe((texts) => {
      this.translations = texts;
    });
  }

  getAllSchedules(): Observable<Schedule[]> {
    return this.http.get(this.heroesUrl)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  getScheduleById(scheduleId: string): Observable<Schedule> {
    return this.http.get(this.heroesUrl + '/' + scheduleId)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  createSchedule(schedule: any): Observable<Schedule> {
    return this.http
      .post(this.heroesUrl, JSON.stringify({
        name: schedule.name,
        alterEgo: schedule.alterEgo
      }), {headers: this.headers})
      .map(response => {
        this.showSnackBar('heroCreated');
        return response;
      })
      .catch(error => this.handleError(error));
  }

  like(schedule: Schedule) {
    if (this.checkIfUserCanVote()) {
      const url = `${this.heroesUrl}/${schedule.id}/like`;
      return this.http
        .post(url, {}, {headers: this.headers})
        .map((response) => {
          localStorage.setItem('votes', '' + (Number(localStorage.getItem('votes')) + 1));
          schedule.likes += 1;
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

  deleteScheduleById(id: any): Observable<Array<Schedule>> {
    const url = `${this.heroesUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .map((response) => {
        this.showSnackBar('scheduleRemoved');
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
