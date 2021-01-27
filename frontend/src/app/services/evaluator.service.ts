import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
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

  getEvaluator(evaluatorId: string): Observable<Evaluator> {
    if (!this.evaluatorsFetched) this.fetchEvaluators();

    let evaluator$: Observable<Evaluator> = new Observable((sub) => {
      this.evaluators.subscribe((evaluators: Evaluator[]) => {
        sub.next(
          evaluators
            .filter(
              (evaluator: Evaluator) => evaluator.evaluator_id == evaluatorId
            )
            .pop()
        );
      });
    });
    return evaluator$;
  }

  getEvaluatorName(evaluatorId: string): Observable<string> {
    if (!this.evaluatorsFetched) this.fetchEvaluators();

    let evaluatorName$: Observable<string> = new Observable((sub) => {
      this.evaluators.subscribe((evaluators: Evaluator[]) => {
        let evaluator: Evaluator = evaluators
          .filter((e: Evaluator) => e.evaluator_id == evaluatorId)
          .pop();
        if (evaluator != undefined)
          sub.next(evaluator.first_name + ' ' + evaluator.last_name);
      });
    });
    return evaluatorName$;
  }

  fetchEvaluators(): void {
    this.evaluatorsFetched = true;

    this.http
      .get('http://localhost:3001/evaluator')
      .subscribe((result: Evaluator[]) => this.evaluators.next(result));
  }
}
