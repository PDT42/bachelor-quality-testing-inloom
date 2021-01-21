import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ExerciseService } from 'src/app/services/exercise.service';
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
    public tdsService: TestDataSetService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.exerciseId = params['id'];
    });
  }

  deleteExercise(): void {
    console.warn("Delete Exercise not yet implemented!")
  }
}
