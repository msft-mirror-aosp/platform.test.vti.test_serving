import {async, TestBed} from '@angular/core/testing';
import {APP_BASE_HREF} from '@angular/common';
import {DeviceListComponent} from './device-list.component';
import {DeviceModule} from '../device.module';
import {TestsModule} from '../../shared/modules/tests.module';
import {TranslateModule} from '@ngx-translate/core';
import {APP_CONFIG, AppConfig} from '../../config/app.config';

describe('DeviceListComponent', () => {
  let fixture;
  let component;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        TestsModule,
        TranslateModule.forRoot(),
        DeviceModule
      ],
      providers: [
        {provide: APP_CONFIG, useValue: AppConfig},
        {provide: APP_BASE_HREF, useValue: '/'}
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceListComponent);
    fixture.detectChanges();
    component = fixture.debugElement.componentInstance;
  }));

  it('should create device list component', (() => {
    expect(component).toBeTruthy();
  }));
});
