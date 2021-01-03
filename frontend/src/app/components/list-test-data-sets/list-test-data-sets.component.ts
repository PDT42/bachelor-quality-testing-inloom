import { Component, OnInit } from '@angular/core';
import { StatisticsService } from 'src/app/services/statistics.service';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-listtestdatasets',
  templateUrl: './list-test-data-sets.component.html',
  styleUrls: ['./list-test-data-sets.component.css'],
})
export class ListTestTataSetsComponent implements OnInit {

  constructor(
    public tdsService: TestDataSetService,
    public statisticsService: StatisticsService
    ) {}

  ngOnInit(): void {}
}
