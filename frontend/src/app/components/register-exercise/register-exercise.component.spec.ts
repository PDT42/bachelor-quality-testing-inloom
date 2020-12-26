import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterExerciseComponent } from './register-exercise.component';

describe('RegisterExerciseComponent', () => {
  let component: RegisterExerciseComponent;
  let fixture: ComponentFixture<RegisterExerciseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterExerciseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterExerciseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
