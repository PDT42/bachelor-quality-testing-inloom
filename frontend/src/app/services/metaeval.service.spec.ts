import { TestBed } from '@angular/core/testing';

import { MetaEvalService } from './metaeval.service';

describe('MetaEvalService', () => {
  let service: MetaEvalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MetaEvalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
