import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

import {AppConfig} from '../../config/app.config';

import {Device} from './device.model';
import {Observable} from 'rxjs/Observable';
import {MatSnackBar, MatSnackBarConfig} from '@angular/material';
import {TranslateService} from '@ngx-translate/core';

@Injectable()
export class DeviceService {
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

    this.translateService.get(['heroCreated', 'saved', 'heroLikeMaximum', 'heroRemoved'], {
      'value': AppConfig.votesLimit
    }).subscribe((texts) => {
      this.translations = texts;
    });
  }

  getAllDevices(): Observable<Device[]> {
    return this.http.get(this.heroesUrl)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  getDeviceById(deviceId: string): Observable<Device> {
    return this.http.get(this.heroesUrl + '/' + deviceId)
      .map(response => {
        return response;
      })
      .catch(error => this.handleError(error));
  }

  createDevice(device: any): Observable<Device> {
    return this.http
      .post(this.heroesUrl, JSON.stringify({
        name: device.name,
        alterEgo: device.alterEgo
      }), {headers: this.headers})
      .map(response => {
        this.showSnackBar('deviceCreated');
        return response;
      })
      .catch(error => this.handleError(error));
  }

  like(device: Device) {
    if (this.checkIfUserCanVote()) {
      const url = `${this.heroesUrl}/${device.id}/like`;
      return this.http
        .post(url, {}, {headers: this.headers})
        .map((response) => {
          localStorage.setItem('votes', '' + (Number(localStorage.getItem('votes')) + 1));
          device.likes += 1;
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

  deleteDeviceById(id: any): Observable<Array<Device>> {
    const url = `${this.heroesUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .map((response) => {
        this.showSnackBar('heroRemoved');
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
