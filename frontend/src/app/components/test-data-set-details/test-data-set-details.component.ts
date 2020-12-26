import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TestDataSet } from '../../classes/test-data-set';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-test-data-set-details',
  templateUrl: './test-data-set-details.component.html',
  styleUrls: ['./test-data-set-details.component.css'],
})
export class TestDataSetDetailsComponent implements OnInit {
  testDataSetId: string;
  evaluationType: string;
  testDataSet: TestDataSet;
  testDataSetTitle: string;

  constructor(
    private route: ActivatedRoute,
    private tdsService: TestDataSetService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.testDataSetId = params['id'];
      this.evaluationType = params['type'];

      this.tdsService
        .getTestDataSet()
        .subscribe((testDataSets: TestDataSet[]) => {
          // Getting the tds this page is supposed
          // to present from the list of available
          // TestDataSets.
          this.testDataSet = testDataSets
            .filter((tds) => tds.test_data_set_id === this.testDataSetId)
            .pop();
          // Update the string that is intended to
          // act as this pages title.
          if (this.testDataSet) {
            this.testDataSetTitle =
              'TDS - Exercise: ' +
              this.testDataSet.exercise_id +
              ' - Student: ' +
              this.testDataSet.student_id;
          }
        });
    });
  }
}
