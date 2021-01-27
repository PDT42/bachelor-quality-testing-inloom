import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Evaluation } from '../classes/evaluation';
import { MetaEvalService } from './metaeval.service';
import { TestDataSetService } from './test-data-set-service.service';

@Injectable({
  providedIn: 'root',
})
export class EvaluationService {
  evaluations: BehaviorSubject<Evaluation[]>;
  evaluationsFetched: Boolean = false;

  constructor(
    private http: HttpClient,
    private tdsService: TestDataSetService,
    private metaEvalService: MetaEvalService
  ) {
    this.evaluations = new BehaviorSubject<Evaluation[]>([]);
    this.fetchEvaluations();
  }

  getEvaluationName(evaluation: Evaluation) {
    return evaluation.evaluation_type + ' - ' + (new Date(evaluation.created_time * 1000)).toUTCString()
  }

  getEvaluations(): BehaviorSubject<Evaluation[]> {
    if (!this.evaluationsFetched) this.fetchEvaluations();

    return this.evaluations;
  }

  getEvaluation(evaluationId: string): Observable<Evaluation> {
    let evaluation$: Observable<Evaluation> = new Observable((sub) => {
      this.evaluations.subscribe((evaluations: Evaluation[]) => {
        let evaluation: Evaluation = evaluations
          .filter((e) => e.evaluation_id == evaluationId)
          .pop();
        if (evaluation) {
          sub.next(evaluation);
        }
      });
    });
    return evaluation$;
  }

  getEvaluationsOfExercise(exerciseId: string): Observable<Evaluation[]> {
    if (!this.evaluationsFetched) this.fetchEvaluations();

    let evaluations$: Observable<Evaluation[]> = new Observable((sub) => {
      this.evaluations.subscribe((evaluations: Evaluation[]) => {
        sub.next(
          evaluations.filter(
            (evaluation: Evaluation) => evaluation.exercise_id == exerciseId
          )
        );
      });
    });
    return evaluations$;
  }

  getEvaluationsOfEvaluator(evaluatorId: string): Observable<Evaluation[]> {
    if (!this.evaluationsFetched) this.fetchEvaluations();

    let evaluations$: Observable<Evaluation[]> = new Observable((sub) => {
      this.evaluations.subscribe((evaluations: Evaluation[]) => {
        let evals: Evaluation[] = evaluations.filter(
          (evaluation: Evaluation) => evaluation.evaluator_id == evaluatorId
        );
        if (evals) {
          sub.next(evals);
        }
      });
    });
    return evaluations$;
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
          this.tdsService.fetchData();
          this.metaEvalService.fetchTDSMetaEvals();
          return result;
        });
    }
  }
}
