import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Evaluation } from '../classes/evaluation';

@Injectable({
  providedIn: 'root',
})
export class EvaluationService {
  evaluations: BehaviorSubject<Evaluation[]>;
  evaluationsFetched: Boolean = false;

  constructor(private http: HttpClient) {
    this.evaluations = new BehaviorSubject<Evaluation[]>([]);
    this.fetchEvaluations();
  }

  getEvaluations(): BehaviorSubject<Evaluation[]> {
    if (!this.evaluationsFetched) this.fetchEvaluations();

    return this.evaluations;
  }

  fetchEvaluations(): void {
    this.evaluationsFetched = true;

    this.http
      .get('http://localhost:3001/eval')
      .subscribe((result: Evaluation[]) => this.evaluations.next(result));
  }

  registerEvaluation(evaluation: Evaluation): void {
    if (evaluation.evaluation_type === 'M') {
      this.http
        .post('http://localhost:3001/eval/register/man', evaluation)
        .subscribe((result) => {
          this.fetchEvaluations();
          return result;
        });
    }
  }
}
