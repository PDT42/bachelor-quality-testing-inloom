import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListTestTataSetsComponent } from './list-test-data-sets.component';

describe('ListtestdatasetsComponent', () => {
  let component: ListTestTataSetsComponent;
  let fixture: ComponentFixture<ListTestTataSetsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListTestTataSetsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListTestTataSetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
