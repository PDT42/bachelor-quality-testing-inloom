import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TestDataSet } from '../classes/test-data-set';
import { TestDataSetService } from './test-data-set-service.service';

@Injectable({
  providedIn: 'root',
})
export class MetaEvalService {
  metaEvalCache: Map<string, BehaviorSubject<Object>>;

  constructor(
    private http: HttpClient,
    private tdsService: TestDataSetService
  ) {
    this.metaEvalCache = new Map();
    this.fetchTDSMetaEvals();
  }

  getTDSMetaEval(testDataSetId: string): BehaviorSubject<Object> {
    if (!this.metaEvalCache.has(testDataSetId)) {
      this.metaEvalCache.set(testDataSetId, new BehaviorSubject<Object>([]));
      this.refreshTDSMetaEvalCache();
    }

    return this.metaEvalCache.get(testDataSetId);
  }

  getExerciseMetaEvals(exerciseId: string): Observable<Map<string, Object>> {
    let metaEvals$: Observable<Map<string, Object>> = new Observable((sub) =>
      this.tdsService
        .getTestDataSetsOfExercise(exerciseId)
        .subscribe((testDataSets: TestDataSet[]) => {
          let exerciseMetaEvals: Map<string, Object> = new Map();
          testDataSets.map((testDataSet: TestDataSet) => {
            this.getTDSMetaEval(testDataSet.test_data_set_id).subscribe(
              (metaEval: Object) => {
                metaEval['student-id'] = testDataSet.student_id;
                exerciseMetaEvals.set(testDataSet.test_data_set_id, metaEval);
                sub.next(exerciseMetaEvals);
              }
            );
          });
        })
    );

    return metaEvals$;
  }

  getGradeQuotient(testDataSetId: string, evalId: string): Observable<number> {
    let avgGradeQuotient$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEvals: Object) => {
        if (metaEvals['grade-quotients']) {
          sub.next(metaEvals['grade-quotients'][evalId]);
        }
      });
    });
    return avgGradeQuotient$;
  }

  getKPIValue(testDataSetId: string, kpiKey: string): Observable<number> {
    let kpiValue$: Observable<number> = new Observable((sub) => {
      if (testDataSetId) {
        this.getTDSMetaEval(testDataSetId).subscribe((metaEvals: Object) => {
          if (Object.keys(metaEvals).length > 0) {
            sub.next(metaEvals[kpiKey]);
          }
        });
      }
    });
    return kpiValue$;
  }

  refreshTDSMetaEvalCache(): void {
    this.metaEvalCache.forEach((_, testDataSetId) => {
      this.http
        .get('http://localhost:3001/metaeval/tds:' + testDataSetId)
        .subscribe((result) => {
          this.metaEvalCache.get(testDataSetId).next(result);
        });
    });
  }

  fetchTDSMetaEvals(): void {
    this.http
      .get('http://localhost:3001/metaeval')
      .subscribe((result: Object) => {
        if (result != null) {
          Object.entries(result).map(([tdsId, value]) => {
            if (!this.metaEvalCache.has(tdsId)) {
              this.metaEvalCache.set(tdsId, new BehaviorSubject<Object>([]));
            }
            this.metaEvalCache.get(tdsId).next(value);
          });
        }
      });
  }
}
