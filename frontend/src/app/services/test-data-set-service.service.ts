import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Evaluation } from '../classes/evaluation';
import { TestDataSet } from '../classes/test-data-set';
import { EvaluationService } from './evaluation.service';

@Injectable({
  providedIn: 'root',
})
export class TestDataSetService {
  testDataSets: BehaviorSubject<TestDataSet[]>;
  testDataSetsFetched: Boolean = false;

  constructor(private http: HttpClient) {
    this.testDataSets = new BehaviorSubject<TestDataSet[]>([]);
  }

  getTestDataSets(): BehaviorSubject<TestDataSet[]> {
    if (!this.testDataSetsFetched) this.fetchData();

    return this.testDataSets;
  }

  getTestDataSetsOfExercise(exerciseId: string): Observable<TestDataSet[]> {
    let testDataSets$: Observable<TestDataSet[]> = new Observable((sub) => {
      this.getTestDataSets().subscribe((testDataSets: TestDataSet[]) => {
        sub.next(
          testDataSets.filter(
            (tds: TestDataSet) => tds.exercise_id === exerciseId
          )
        );
      });
    });
    return testDataSets$;
  }

  getTestDataSetsOfEvaluations(
    evaluations: Evaluation[]
  ): Observable<TestDataSet[]> {
    let testDataSets$: Observable<TestDataSet[]> = new Observable((sub) => {
      this.getTestDataSets().subscribe((testDataSets: TestDataSet[]) => {
        let testdataSets: TestDataSet[] = testDataSets.filter(
          (testDataSet: TestDataSet) =>
            evaluations &&
            evaluations
              .map((evaluation: Evaluation) => evaluation.test_data_set_id)
              .includes(testDataSet.test_data_set_id)
        );
        if (testDataSets.length > 0) {
          sub.next(testDataSets);
        }
      });
    });
    return testDataSets$;
  }

  getTestDataSet(testDataSetId: string): Observable<TestDataSet> {
    let testDataSet$: Observable<TestDataSet> = new Observable((sub) => {
      this.getTestDataSets().subscribe((testDataSets: TestDataSet[]) => {
        sub.next(
          testDataSets
            .filter(
              (testDataSet: TestDataSet) =>
                testDataSet.test_data_set_id === testDataSetId
            )
            .pop()
        );
      });
    });
    return testDataSet$;
  }

  fetchData(): void {
    this.testDataSetsFetched = true;

    this.http
      .get('http://localhost:3001/testdataset')
      .subscribe((result: TestDataSet[]) => {
        this.testDataSets.next(result);
      });
  }

  deleteTDS(test_data_set_id: string): void {
    const idData: FormData = new FormData();

    idData.append('test_data_set_id', test_data_set_id);
    this.http
      .post('http://127.0.0.1:3001/testdataset/delete', idData)
      .subscribe((result) => {
        this.fetchData();
        return result;
      });
  }
}
