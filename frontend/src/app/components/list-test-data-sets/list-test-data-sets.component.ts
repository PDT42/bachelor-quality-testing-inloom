import { Component, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { TestDataSet } from 'src/app/classes/test-data-set';
import { MetaEvalService } from 'src/app/services/metaeval.service';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-listtestdatasets',
  templateUrl: './list-test-data-sets.component.html',
  styleUrls: ['./list-test-data-sets.component.css'],
})
export class ListTestTataSetsComponent implements OnInit {
  @Input()
  testDataSets$: Observable<TestDataSet[]>;

  constructor(
    public metaEvalService: MetaEvalService
  ) {}

  ngOnInit(): void {}
}
