import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleComparisonComponent } from './single-comparison.component';

describe('SingleComparisonComponent', () => {
  let component: SingleComparisonComponent;
  let fixture: ComponentFixture<SingleComparisonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SingleComparisonComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SingleComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
