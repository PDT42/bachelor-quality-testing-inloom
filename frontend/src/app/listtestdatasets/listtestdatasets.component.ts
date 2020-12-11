import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { TestDataSetService } from '../services/test-data-set-service.service';
import { TestDataSet } from '../interfaces/test-data-set';

@Component({
  selector: 'app-listtestdatasets',
  templateUrl: './listtestdatasets.component.html',
  styleUrls: ['./listtestdatasets.component.css'],
})
export class ListtestdatasetsComponent implements OnInit {
  constructor(public tds_service: TestDataSetService) {}

  ngOnInit(): void { }
}
