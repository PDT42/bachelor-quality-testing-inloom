import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestDataSetDashboardComponent } from './test-data-set-dashboard.component';

describe('TestDataSetDashboardComponent', () => {
  let component: TestDataSetDashboardComponent;
  let fixture: ComponentFixture<TestDataSetDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestDataSetDashboardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestDataSetDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
