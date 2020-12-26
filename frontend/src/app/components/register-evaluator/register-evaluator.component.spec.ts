import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterEvaluatorComponent } from './register-evaluator.component';

describe('RegisterEvaluatorComponent', () => {
  let component: RegisterEvaluatorComponent;
  let fixture: ComponentFixture<RegisterEvaluatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterEvaluatorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterEvaluatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
