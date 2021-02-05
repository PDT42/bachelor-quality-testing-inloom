import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { TestDataSet } from 'src/app/classes/test-data-set';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { ExerciseService } from 'src/app/services/exercise.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';
import { TestDataSetService } from 'src/app/services/test-data-set-service.service';

@Component({
  selector: 'app-exercise-details',
  templateUrl: './exercise-details.component.html',
  styleUrls: ['./exercise-details.component.css'],
})
export class ExerciseDetailsComponent implements OnInit {
  exerciseId: string;

  constructor(
    private route: ActivatedRoute,
    public exerciseService: ExerciseService,
    public tdsService: TestDataSetService,
    public evaluationService: EvaluationService,
    public metaEvalService: MetaEvalService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.exerciseId = params['id'];
    });
  }

  getPctDifferenceColor(exerciseId: string): Observable<string> {
    let color$: Observable<string> = new Observable((sub) => {
      this.metaEvalService
        .getExerciseAveragePctDiff(exerciseId)
        .subscribe((avgPctDiff: number) => {
          if (avgPctDiff < 5) {
            sub.next('#5fab46');
          } else if (5 <= avgPctDiff && avgPctDiff < 10) {
            sub.next('#ebda46');
          } else if (10 <= avgPctDiff && avgPctDiff < 15) {
            sub.next('#de5047');
          } else {
            sub.next('#d91414');
          }
        });
    });
    return color$;
  }
}
