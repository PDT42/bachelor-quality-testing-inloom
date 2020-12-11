import { TestBed } from '@angular/core/testing';

import { TestDataSetService } from './test-data-set-service.service';

describe('TestDataSetServiceService', () => {
  let service: TestDataSetService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TestDataSetService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
