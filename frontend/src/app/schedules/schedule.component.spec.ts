import {async, TestBed} from '@angular/core/testing';
import {APP_BASE_HREF} from '@angular/common';
import {ScheduleComponent} from './schedule.component';
import {ScheduleModule} from './schedule.module';
import {TestsModule} from '../shared/modules/tests.module';
import {CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';

describe('HeroesComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        TestsModule,
        ScheduleModule
      ],
      providers: [
        {provide: APP_BASE_HREF, useValue: '/'}
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();
  }));

  it('should create schedule component', (() => {
    const fixture = TestBed.createComponent(ScheduleComponent);
    fixture.detectChanges();
    const component = fixture.debugElement.componentInstance;
    expect(component).toBeTruthy();
  }));
});
