import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { EvaluatorService } from 'src/app/services/evaluator.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';
import { TestDataSetService } from 'src/app/services/test-data-set-service.service';

@Component({
  selector: 'app-evaluator-details',
  templateUrl: './evaluator-details.component.html',
  styleUrls: ['./evaluator-details.component.css'],
})
export class EvaluatorDetailsComponent implements OnInit {
  evaluatorId: string;

  constructor(
    private route: ActivatedRoute,
    public evaluatorService: EvaluatorService,
    public evaluationService: EvaluationService,
    public tdsService: TestDataSetService,
    public metaEvalService: MetaEvalService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.evaluatorId = params['id'];
    });
  }
}
