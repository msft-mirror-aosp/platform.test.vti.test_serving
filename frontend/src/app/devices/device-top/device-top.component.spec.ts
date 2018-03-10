import {async, fakeAsync, TestBed, tick} from '@angular/core/testing';
import {APP_BASE_HREF} from '@angular/common';
import {DeviceTopComponent} from './device-top.component';
import {DeviceService} from '../shared/device.service';
import {TestsModule} from '../../shared/modules/tests.module';
import {TranslateModule} from '@ngx-translate/core';
import {APP_CONFIG, AppConfig} from '../../config/app.config';
import {CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';

describe('HeroTopComponent', () => {
  let fixture;
  let component;
  let heroService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        TestsModule,
        TranslateModule.forRoot(),
      ],
      declarations: [
        DeviceTopComponent
      ],
      providers: [
        {provide: APP_CONFIG, useValue: AppConfig},
        {provide: APP_BASE_HREF, useValue: '/'},
        DeviceService
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceTopComponent);
    fixture.detectChanges();
    component = fixture.debugElement.componentInstance;
    heroService = TestBed.get(DeviceService);
  }));

  it('should create hero top component', (() => {
    expect(component).toBeTruthy();
  }));

  it('should initialice component', fakeAsync(() => {
    fixture.detectChanges();
    spyOn(heroService, 'getAllHeroes').and.returnValue(Promise.resolve(true));
    tick();
    fixture.detectChanges();
    expect(component.heroes.length).toBe(AppConfig.topHeroesLimit);
  }));

  it('should like a hero', async(() => {
    localStorage.setItem('votes', String(AppConfig.votesLimit - 1));
    component.like({id: 1}).then((result) => {
      expect(result).toBe(true);
    });
  }));

  it('should not like a hero', async(() => {
    localStorage.setItem('votes', String(AppConfig.votesLimit));
    component.like({id: 1}).then(() => {
    }, (error) => {
      expect(error).toBe('maximum votes');
    });
    expect(heroService.checkIfUserCanVote()).toBe(false);
  }));
});
