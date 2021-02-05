import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ExerciseService } from 'src/app/services/exercise.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-list-exercises',
  templateUrl: './list-exercises.component.html',
  styleUrls: ['./list-exercises.component.css'],
})
export class ListExercisesComponent implements OnInit {
  constructor(
    public exerciseService: ExerciseService,
    public metaEvalService: MetaEvalService
  ) {}

  ngOnInit(): void {}

  getPctDifferenceColor(exerciseId: string): Observable<string> {
    let color$: Observable<string> = new Observable((sub) => {
      this.metaEvalService
        .getExerciseAveragePctDiff(exerciseId)
        .subscribe((avgPctDiff: number) => {
          avgPctDiff = Math.abs(avgPctDiff);

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
