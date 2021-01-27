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
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-list-evaluations',
  templateUrl: './list-evaluations.component.html',
  styleUrls: ['./list-evaluations.component.css'],
})
export class ListEvaluationsComponent implements OnInit {
  @Input()
  evaluations: Evaluation[]

  constructor(
    public evalService: EvaluationService,
    public evaluatorService: EvaluatorService,
    public exerciseService: ExerciseService,
    public metaEvalService: MetaEvalService
  ) {}

  ngOnInit(): void {}


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

  formatDate(created_time: number) {
    return new Date(created_time * 10 ** 3);
  }
}
