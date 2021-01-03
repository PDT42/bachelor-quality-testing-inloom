import { keyframes } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StatisticsService {
  statistics: Map<string, BehaviorSubject<Object>>;

  constructor(private http: HttpClient) {
    this.statistics = new Map();
  }

  getTDSStatistics(testDataSetId: string): BehaviorSubject<Object> {
    if (!this.statistics.has(testDataSetId)) {
      this.statistics.set(testDataSetId, new BehaviorSubject<Object>([]));
      this.fetchTDSStatistic();
    }

    return this.statistics.get(testDataSetId);
  }

  getGradeQuotient(
    testDataSetId: string,
    evalId: string
  ): Observable<number> {
    let avgGradeQuotient$: Observable<number> = new Observable((sub) => {
      this.getTDSStatistics(testDataSetId).subscribe((statistics: Object) => {
        if (statistics['grade-quotients']) {
          sub.next(statistics['grade-quotients'][evalId]);
        }
      });
    });
    return avgGradeQuotient$;
  }

  getAverageManGrade(testDataSetId: string): Observable<number> {
    let avgManGrade$: Observable<number> = new Observable((sub) => {
      if (testDataSetId) {
        this.getTDSStatistics(testDataSetId).subscribe((statistics: Object) => {
          if (Object.keys(statistics).length > 0) {
            sub.next(statistics['average-man-grade']);
          }
        });
      }
    });
    return avgManGrade$;
  }

  fetchTDSStatistic(): void {
    this.statistics.forEach((_, testDataSetId) => {
      this.http
        .get('http://localhost:3001/statistics/tds:' + testDataSetId)
        .subscribe((result) => {
          this.statistics.get(testDataSetId).next(result);
        });
    });
  }
}
