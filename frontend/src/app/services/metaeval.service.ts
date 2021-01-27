import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Evaluation } from '../classes/evaluation';
import { TestDataSet } from '../classes/test-data-set';
import { TestDataSetService } from './test-data-set-service.service';

@Injectable({
  providedIn: 'root',
})
export class MetaEvalService {
  metaEvalCache: Map<string, BehaviorSubject<Object>>;
  excMetaEvalCache: Map<string, BehaviorSubject<Object>>;

  constructor(
    private http: HttpClient,
    private tdsService: TestDataSetService
  ) {
    this.metaEvalCache = new Map();
    this.excMetaEvalCache = new Map();

    this.fetchTDSMetaEvals();
  }

  /*
  Get a TDS Level Meta Eval.
  */
  getTDSMetaEval(testDataSetId: string): BehaviorSubject<Object> {
    if (!this.metaEvalCache.has(testDataSetId)) {
      this.metaEvalCache.set(testDataSetId, new BehaviorSubject<Object>([]));
      this.refreshTDSMetaEvalCache();
    }

    return this.metaEvalCache.get(testDataSetId);
  }

  /*
  Get an Exercise Level Meta Eval.
  */
  getEXCMetaEval(exerciseId: string): BehaviorSubject<Object> {
    if (!this.excMetaEvalCache.has(exerciseId)) {
      this.excMetaEvalCache.set(exerciseId, new BehaviorSubject<Object>([]));
      this.refreshEXCMetaEvalCache();
    }

    return this.excMetaEvalCache.get(exerciseId);
  }

  /*
  Get the tdsMetaEvals of all TDS of an exercise.
  */
  getExerciseMetaEvals(exerciseId: string): Observable<Map<string, Object>> {
    let metaEvals$: Observable<Map<string, Object>> = new Observable((sub) =>
      this.tdsService
        .getTestDataSetsOfExercise(exerciseId)
        .subscribe((testDataSets: TestDataSet[]) => {
          let exerciseMetaEvals: Map<string, Object> = new Map();
          testDataSets.map((testDataSet: TestDataSet) => {
            this.getTDSMetaEval(testDataSet.test_data_set_id).subscribe(
              (metaEval: Object) => {
                exerciseMetaEvals.set(testDataSet.test_data_set_id, metaEval);
                sub.next(exerciseMetaEvals);
              }
            );
          });
        })
    );

    return metaEvals$;
  }

  /*
  Get the exercise level avg-man-grade from the exercise
  level meta evaluation.
  */
  getExerciseAverageGradeQuotient(exerciseId: string): Observable<number> {
    let avgGradeQt$: Observable<number> = new Observable((sub) => {
      this.getEXCMetaEval(exerciseId).subscribe(
        (excMetaEval: Map<string, Object>) => {
          if (Object.keys(excMetaEval).length > 0) {
            sub.next(excMetaEval['avg-grade-quotient']);
          }
        }
      );
    });
    return avgGradeQt$;
  }

  /*
  Get the exercise level avg-man-pct-difference from the exercise
  level meta evaluation.
  */
  getExerciseAveragePctDiff(exerciseId: string): Observable<number> {
    let avgPctDiff$: Observable<number> = new Observable((sub) => {
      this.getEXCMetaEval(exerciseId).subscribe(
        (excMetaEval: Map<string, Object>) => {
          if (Object.keys(excMetaEval).length > 0) {
            sub.next(excMetaEval['avg-percentage-differences']);
          }
        }
      );
    });
    return avgPctDiff$;
  }

  /*
  Get the TDS Level meta evals for all tds of an evalautor.
  */
  getEvaluationsMetaEvals(
    evaluations: Evaluation[]
  ): Observable<Map<string, Object>> {
    let metaEvals$: Observable<Map<string, Object>> = new Observable((sub) =>
      this.tdsService
        .getTestDataSetsOfEvaluations(evaluations)
        .subscribe((testDataSets: TestDataSet[]) => {
          let exerciseMetaEvals: Map<string, Object> = new Map();
          testDataSets.map((testDataSet: TestDataSet) => {
            this.getTDSMetaEval(testDataSet.test_data_set_id).subscribe(
              (metaEval: Object) => {
                exerciseMetaEvals.set(testDataSet.test_data_set_id, metaEval);
                sub.next(exerciseMetaEvals);
              }
            );
          });
        })
    );

    return metaEvals$;
  }

  getEvaluationTotalPoints(
    testDataSetId: string,
    evalId: string
  ): Observable<number> {
    let totalPoints$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEval: Object) => {
        if (metaEval['eval-stats']) {
          sub.next(metaEval['eval-stats'][evalId]['total-points']);
        }
      });
    });

    return totalPoints$;
  }

  getEvaluationGrade(
    testDataSetId: string,
    evalId: string
  ): Observable<number> {
    let evalGrade$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEval: Object) => {
        if (metaEval['eval-stats']) {
          sub.next(metaEval['eval-stats'][evalId]['grade']);
        }
      });
    });

    return evalGrade$;
  }

  /*
  Get the TDS level grade quotient of an evaluation.
  */
  getComparisonGradeQuotient(testDataSetId: string, comparisonId: string): Observable<number> {
    let avgGradeQuotient$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEval: Object) => {
        if (metaEval['comparison-stats']) {
          sub.next(metaEval['comparison-stats']['grade-quotients'][comparisonId]);
        }
      });
    });

    return avgGradeQuotient$;
  }

  getComparisonPtDiff(
    testDataSetId: string,
    comparisonId: string
  ): Observable<number> {
    let ptDiff$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEval: Object) => {
        if (metaEval['comparison-stats']) {
          sub.next(metaEval['comparison-stats']['point-diffs'][comparisonId]);
        }
      });
    });

    return ptDiff$;
  }

  getComparisonPctDiff(
    testDataSetId: string,
    comparisonId: string
  ): Observable<number> {
    let pctDiff$: Observable<number> = new Observable((sub) => {
      this.getTDSMetaEval(testDataSetId).subscribe((metaEval: Object) => {
        if (metaEval['comparison-stats']) {
          sub.next(metaEval['comparison-stats']['point-pct-diffs'][comparisonId]);
        }
      });
    });

    return pctDiff$;
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

  refreshEXCMetaEvalCache(): void {
    this.excMetaEvalCache.forEach((_, exerciseId) => {
      this.http
        .get('http://localhost:3001/metaeval/exc:' + exerciseId)
        .subscribe((result) => {
          this.excMetaEvalCache.get(exerciseId).next(result);
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
