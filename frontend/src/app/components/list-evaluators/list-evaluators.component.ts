import { Component, OnInit } from '@angular/core';
import { EvaluatorService } from 'src/app/services/evaluator.service';

@Component({
  selector: 'app-list-evaluators',
  templateUrl: './list-evaluators.component.html',
  styleUrls: ['./list-evaluators.component.css']
})
export class ListEvaluatorsComponent implements OnInit {

  constructor(
    public evaluatorService: EvaluatorService
  ) { }

  ngOnInit(): void {
  }

}
