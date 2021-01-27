import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MultipleComparisonComponent } from './multiple-comparison.component';

describe('MultipleComparisonComponent', () => {
  let component: MultipleComparisonComponent;
  let fixture: ComponentFixture<MultipleComparisonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MultipleComparisonComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MultipleComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
