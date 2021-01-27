import { Component, Input, OnInit } from '@angular/core';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { ExerciseService } from 'src/app/services/exercise.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';
import { TestDataSetService } from 'src/app/services/test-data-set-service.service';

@Component({
  selector: 'app-tds-comparison',
  templateUrl: './tds-comparison.component.html',
  styleUrls: ['./tds-comparison.component.css']
})
export class TdsComparisonComponent implements OnInit {

  @Input()
  testDataSetId: string;
  @Input()
  manEvalKey: string = 'avg-man-eval';
  @Input()
  autoEvalKey: string = 'latest-auto-eval';

  constructor(
    public exerciseService: ExerciseService,
    public evaluationService: EvaluationService,
    public tdsService: TestDataSetService,
    public metaEvalService: MetaEvalService
  ) { }

  ngOnInit(): void {
  }
}
