import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterAutoEval } from './register-auto-eval.component';

describe('FileUploadComponent', () => {
  let component: RegisterAutoEval;
  let fixture: ComponentFixture<RegisterAutoEval>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterAutoEval ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterAutoEval);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
