import {Component} from '@angular/core';

import {Device} from '../shared/device.model';

import {DeviceService} from '../shared/device.service';
import {AppConfig} from '../../config/app.config';

@Component({
  selector: 'app-device-top',
  templateUrl: './device-top.component.html',
  styleUrls: ['./device-top.component.scss']
})
export class DeviceTopComponent {

  devices: Device[] = null;
  canVote = false;

  constructor(private deviceService: DeviceService) {
    this.canVote = this.deviceService.checkIfUserCanVote();

    this.deviceService.getAllDevices().subscribe((devices) => {
      this.devices = devices.sort((a, b) => {
        return b.likes - a.likes;
      }).slice(0, AppConfig.topHeroesLimit);
    });
  }

  like(device: Device): Promise<any> {
    return new Promise((resolve, reject) => {
      this.deviceService.like(device).subscribe(() => {
        this.canVote = this.deviceService.checkIfUserCanVote();
        resolve(true);
      }, (error) => {
        reject(error);
      });
    });
  }
}
