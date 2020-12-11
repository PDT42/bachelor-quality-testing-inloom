import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListtestdatasetsComponent } from './listtestdatasets.component';

describe('ListtestdatasetsComponent', () => {
  let component: ListtestdatasetsComponent;
  let fixture: ComponentFixture<ListtestdatasetsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListtestdatasetsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListtestdatasetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
