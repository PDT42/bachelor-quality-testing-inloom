import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, Subject } from 'rxjs';
import { TestDataSet } from '../interfaces/test-data-set';

@Injectable({
  providedIn: 'root',
})
export class TestDataSetService {
  testDataSets: BehaviorSubject<TestDataSet[]>;
  fetched: Boolean = false;

  constructor(private http: HttpClient) {
    console.log("init")
    this.testDataSets = new BehaviorSubject<TestDataSet[]>([]);
  }

  getTestDataSet(): Subject<TestDataSet[]> {
    if (!this.fetched) this.fetchData();

    return this.testDataSets;
  }

  fetchData(): void {
    this.fetched = true;

    this.http
      .get('http://localhost:3001/testdatasets')
      .subscribe((result: TestDataSet[]) => {
        this.testDataSets.next(result);
      });
  }
}
