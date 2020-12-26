import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterManEvalComponent } from './register-man-eval.component';

describe('RegisterManEvalComponent', () => {
  let component: RegisterManEvalComponent;
  let fixture: ComponentFixture<RegisterManEvalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterManEvalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterManEvalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
