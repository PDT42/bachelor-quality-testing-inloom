import { Component, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Evaluation } from 'src/app/classes/evaluation';
import { Evaluator } from 'src/app/classes/evaluator';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { EvaluatorService } from 'src/app/services/evaluator.service';

@Component({
  selector: 'app-list-evaluations',
  templateUrl: './list-evaluations.component.html',
  styleUrls: ['./list-evaluations.component.css'],
})
export class ListEvaluationsComponent implements OnInit {
  @Input()
  testDataSetId: string;

  @Input()
  evaluationType: string;

  evaluations: Evaluation[];

  constructor(
    public evalService: EvaluationService,
    public evaluatorService: EvaluatorService
  ) {}

  ngOnInit(): void {
    this.evalService.getEvaluations().subscribe((evaluations: Evaluation[]) => {
      this.evaluations = evaluations
        .filter((e) => e.test_data_set_id === this.testDataSetId)
        .filter((e) => e.evaluation_type === this.evaluationType);
    });
  }

  getEvaluator(evaluatorId: string): Observable<Evaluator> {
    let evaluator$: Observable<Evaluator> = new Observable((sub) => {
      this.evaluatorService.getEvaluators().subscribe((result: Evaluator[]) => {
        sub.next(result.filter((e) => e.evaluator_id === evaluatorId).pop());
      });
    });
    return evaluator$;
  }

  getEvaluatorName(evaluatorId: string): Observable<string> {
    let evaluatorName$: Observable<string> = new Observable((sub) => {
      this.getEvaluator(evaluatorId).subscribe((result: Evaluator) => {
        sub.next(result.first_name + " " + result.last_name);
      })
    });
    return evaluatorName$;
  }

  formatDate(created_time: number) {
    return new Date(created_time * 10 ** 3);
  }
}
