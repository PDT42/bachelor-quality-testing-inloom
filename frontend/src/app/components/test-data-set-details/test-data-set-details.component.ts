import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ExerciseService } from 'src/app/services/exercise.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';
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
    public tdsService: TestDataSetService,
    public metaEvalService: MetaEvalService,
    public exerciseService: ExerciseService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.testDataSetId = params['id'];
    });
  }

  getTestDataSetTitle(): Observable<string> {
    let testDataSetTitle$: Observable<string> = new Observable((sub) => {
      this.tdsService
        .getTestDataSet(this.testDataSetId)
        .subscribe((testDataSet: TestDataSet) => {
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
