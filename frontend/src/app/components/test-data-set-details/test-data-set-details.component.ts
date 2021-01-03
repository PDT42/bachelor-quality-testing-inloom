import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { stat } from 'fs';
import { Observable } from 'rxjs';
import { ExerciseService } from 'src/app/services/exercise.service';
import { StatisticsService } from 'src/app/services/statistics.service';
import { TestDataSet } from '../../classes/test-data-set';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-test-data-set-details',
  templateUrl: './test-data-set-details.component.html',
  styleUrls: ['./test-data-set-details.component.css'],
})
export class TestDataSetDetailsComponent implements OnInit {
  testDataSetId: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private tdsService: TestDataSetService,
    public statisticsService: StatisticsService,
    public exerciseService: ExerciseService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.testDataSetId = params['id'];
    });
  }

  getTestDataSet(): Observable<TestDataSet> {
    let testDataSet$: Observable<TestDataSet> = new Observable((sub) => {
      this.tdsService
        .getTestDataSets()
        .subscribe((testDataSets: TestDataSet[]) => {
          if (this.testDataSetId) {
            sub.next(
              testDataSets
                .filter(
                  (testDataSet: TestDataSet) =>
                    testDataSet.test_data_set_id === this.testDataSetId
                )
                .pop()
            );
          }
        });
    });
    return testDataSet$;
  }

  getTestDataSetTitle(): Observable<string> {
    let testDataSetTitle$: Observable<string> = new Observable((sub) => {
      this.getTestDataSet().subscribe((testDataSet: TestDataSet) => {
        if (testDataSet) {
          sub.next(
            'TDS - Exercise: ' +
              testDataSet.exercise_id +
              ' - Student: ' +
              testDataSet.student_id
          );
        }
      });
    });
    return testDataSetTitle$;
  }

  deleteTDS(): void {
    this.tdsService.deleteTDS(this.testDataSetId);
    this.router.navigate(['register']);
  }
}
