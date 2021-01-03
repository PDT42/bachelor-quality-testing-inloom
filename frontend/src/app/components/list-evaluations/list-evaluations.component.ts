import { Component, Input, OnInit } from '@angular/core';
import { max } from 'd3';
import { Observable } from 'rxjs';
import { Evaluation } from 'src/app/classes/evaluation';
import { Evaluator } from 'src/app/classes/evaluator';
import { ExpertSolution } from 'src/app/classes/expert-solution';
import { TestDataSet } from 'src/app/classes/test-data-set';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { EvaluatorService } from 'src/app/services/evaluator.service';
import { ExerciseService } from 'src/app/services/exercise.service';
import { StatisticsService } from 'src/app/services/statistics.service';

@Component({
  selector: 'app-list-evaluations',
  templateUrl: './list-evaluations.component.html',
  styleUrls: ['./list-evaluations.component.css'],
})
export class ListEvaluationsComponent implements OnInit {
  @Input()
  testDataSet: TestDataSet;

  @Input()
  evaluationType: string;

  evaluations: Evaluation[];

  constructor(
    public evalService: EvaluationService,
    public evaluatorService: EvaluatorService,
    public exerciseService: ExerciseService,
    public statisticsService: StatisticsService
  ) {}

  ngOnInit(): void {}

  getEvaluations(): Observable<Evaluation[]> {
    let evaluations$: Observable<Evaluation[]> = new Observable((sub) => {
      this.evalService
        .getEvaluations()
        .subscribe((evaluations: Evaluation[]) => {
          if (this.testDataSet) {
            sub.next(
              evaluations
                .filter(
                  (e: Evaluation) =>
                    e.test_data_set_id === this.testDataSet.test_data_set_id
                )
                .filter(
                  (e: Evaluation) => e.evaluation_type === this.evaluationType
                )
            );
          }
        });
    });
    return evaluations$;
  }

  getEvaluation(evaluationId: string): Observable<Evaluation> {
    let evaluation$: Observable<Evaluation> = new Observable((sub) => {
      this.getEvaluations().subscribe((evaluations: Evaluation[]) => {
        sub.next(
          evaluations.filter((e) => e.evaluation_id === evaluationId).pop()
        );
      });
    });
    return evaluation$;
  }

  getEvaluator(evaluatorId: string): Observable<Evaluator> {
    let evaluator$: Observable<Evaluator> = new Observable((sub) => {
      this.evaluatorService
        .getEvaluators()
        .subscribe((evaluators: Evaluator[]) => {
          sub.next(
            evaluators.filter((e) => e.evaluator_id === evaluatorId).pop()
          );
        });
    });
    return evaluator$;
  }

  getEvaluatorName(evaluatorId: string): Observable<string> {
    let evaluatorName$: Observable<string> = new Observable((sub) => {
      this.getEvaluator(evaluatorId).subscribe((evaluator: Evaluator) => {
        sub.next(evaluator.first_name + ' ' + evaluator.last_name);
      });
    });
    return evaluatorName$;
  }

  formatDate(created_time: number) {
    return new Date(created_time * 10 ** 3);
  }
}
