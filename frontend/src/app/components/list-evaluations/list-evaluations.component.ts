import { Component, Input, OnInit } from '@angular/core';
import { Evaluation } from 'src/app/classes/evaluation';
import { EvaluationService } from 'src/app/services/evaluation.service';

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

  constructor(public evalService: EvaluationService) {}

  ngOnInit(): void {
    console.log('test')
    this.evalService.getEvaluations().subscribe((evaluations: Evaluation[]) => {
      this.evaluations = evaluations
      .filter((e) => e.test_data_set_id === this.testDataSetId)
      .filter((e) => e.evaluation_type === this.evaluationType);
      console.log(this.evaluations)
    });
  }

  formatDate(created_time: number) {
    return new Date(created_time * 10 ** 3)
  }
}
