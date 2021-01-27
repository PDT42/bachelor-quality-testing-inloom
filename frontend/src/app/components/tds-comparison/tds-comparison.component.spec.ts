import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TdsComparisonComponent } from './tds-comparison.component';

describe('TdsComparisonComponent', () => {
  let component: TdsComparisonComponent;
  let fixture: ComponentFixture<TdsComparisonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TdsComparisonComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TdsComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
