import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryByElementComponent } from './category-by-element.component';

describe('CategoryByElementComponent', () => {
  let component: CategoryByElementComponent;
  let fixture: ComponentFixture<CategoryByElementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CategoryByElementComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CategoryByElementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
