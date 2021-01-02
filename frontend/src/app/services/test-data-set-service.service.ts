import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
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

  getTestDataSets(): Subject<TestDataSet[]> {
    if (!this.testDataSetsFetched) this.fetchData();

    return this.testDataSets;
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
