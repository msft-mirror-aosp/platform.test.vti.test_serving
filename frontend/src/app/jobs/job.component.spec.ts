import {async, TestBed} from '@angular/core/testing';
import {APP_BASE_HREF} from '@angular/common';
import {JobComponent} from './job.component';
import {JobModule} from './job.module';
import {TestsModule} from '../shared/modules/tests.module';
import {CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';

describe('HeroesComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        TestsModule,
        JobModule
      ],
      providers: [
        {provide: APP_BASE_HREF, useValue: '/'}
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();
  }));

  it('should create heroes component', (() => {
    const fixture = TestBed.createComponent(JobComponent);
    fixture.detectChanges();
    const component = fixture.debugElement.componentInstance;
    expect(component).toBeTruthy();
  }));
});
