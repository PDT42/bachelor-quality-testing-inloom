import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Evaluator } from '../classes/evaluator';

@Injectable({
  providedIn: 'root',
})
export class EvaluatorService {
  evaluators: BehaviorSubject<Evaluator[]>;
  evaluatorsFetched: boolean = false;

  constructor(private http: HttpClient) {
    this.evaluators = new BehaviorSubject<Evaluator[]>([]);
    this.fetchEvaluators();
  }

  registerEvaluator(evaluator: Evaluator): void {
    this.http
      .post('http://localhost:3001/evaluator/register', evaluator)
      .subscribe((result) => {
        this.fetchEvaluators();
        return result;
      });
  }

  getEvaluators(): BehaviorSubject<Evaluator[]> {
    if (!this.evaluatorsFetched) this.fetchEvaluators();

    return this.evaluators;
  }

  fetchEvaluators(): void {
    this.evaluatorsFetched = true;

    this.http
      .get('http://localhost:3001/evaluator')
      .subscribe((result: Evaluator[]) => this.evaluators.next(result));
  }
}
