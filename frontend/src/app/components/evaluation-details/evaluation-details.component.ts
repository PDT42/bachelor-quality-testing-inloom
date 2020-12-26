import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Evaluation } from '../../classes/evaluation';
import { EvaluationService } from '../../services/evaluation.service';

@Component({
  selector: 'app-evaluation-details',
  templateUrl: './evaluation-details.component.html',
  styleUrls: ['./evaluation-details.component.css'],
})
export class EvaluationDetailsComponent implements OnInit {
  evaluationId: string;
  evaluation: Evaluation = null;
  evaluationTitle: string = '';
  resultCategoryColors = {
    M: '#6e1212',
    E: '#c71c10',
    W: '#ebda46',
    C: '#358f17',
    I: '#3b87a1',
  };

  constructor(
    private route: ActivatedRoute,
    public evalService: EvaluationService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.evaluationId = params['id'];

      this.evalService
        .getEvaluations()
        .subscribe((evaluations: Evaluation[]) => {
          // Getting the eval this page is supposed
          // to present from the list of available
          // Evaluations.
          this.evaluation = evaluations
            .filter((e) => e.evaluation_id === this.evaluationId)
            .pop();
          // Update the string that is intended to
          // act as this pages title.
          if (this.evaluation && this.evaluation.evaluation_type === 'A') {
            this.evaluationTitle =
              'AutoEval - Exercise: ' +
              this.evaluation.exercise_id +
              ' - Student: ' +
              this.evaluation.student_id;
          }
          if (this.evaluation && this.evaluation.evaluation_type === 'M') {
            this.evaluationTitle =
              'ManEval - Exercise: ' +
              this.evaluation.exercise_id +
              ' - Student: ' +
              this.evaluation.student_id;
          }
        });
    });
  }
}
