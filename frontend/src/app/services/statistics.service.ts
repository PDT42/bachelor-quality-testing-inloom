import { keyframes } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

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

  fetchTDSStatistic(): void {
    this.statistics.forEach((_, testDataSetId) => {
      this.http
        .get('http://localhost:3001/statistics/tds:' + testDataSetId)
        .subscribe((result) => {
          this.statistics.get(testDataSetId).next(result);
          console.log(result);
        });
    });
  }
}
