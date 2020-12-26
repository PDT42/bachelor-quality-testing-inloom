import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, Subject } from 'rxjs';
import { TestDataSet } from '../classes/test-data-set';

@Injectable({
  providedIn: 'root',
})
export class TestDataSetService {
  testDataSets: BehaviorSubject<TestDataSet[]>;
  testDataSetsFetched: Boolean = false;

  constructor(private http: HttpClient) {
    this.testDataSets = new BehaviorSubject<TestDataSet[]>([]);
  }

  getTestDataSet(): Subject<TestDataSet[]> {
    if (!this.testDataSetsFetched) this.fetchData();

    return this.testDataSets;
  }

  fetchData(): void {
    this.testDataSetsFetched = true;

    this.http
      .get('http://localhost:3001/testdatasets')
      .subscribe((result: TestDataSet[]) => {
        this.testDataSets.next(result);
      });
  }
}
