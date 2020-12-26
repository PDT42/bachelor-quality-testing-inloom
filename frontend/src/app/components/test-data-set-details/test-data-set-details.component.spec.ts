import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestDataSetDetailsComponent } from './test-data-set-details.component';

describe('TestDataSetDetailsComponent', () => {
  let component: TestDataSetDetailsComponent;
  let fixture: ComponentFixture<TestDataSetDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestDataSetDetailsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestDataSetDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
