import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExerciseLevelComparisonComponent } from './exercise-level-comparison.component';

describe('ExerciseLevelComparisonComponent', () => {
  let component: ExerciseLevelComparisonComponent;
  let fixture: ComponentFixture<ExerciseLevelComparisonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExerciseLevelComparisonComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExerciseLevelComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
