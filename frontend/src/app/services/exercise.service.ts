import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Exercise } from '../classes/exercise';
import { ExpertSolution } from '../classes/expert-solution';

@Injectable({
  providedIn: 'root',
})
export class ExerciseService {
  exercises: BehaviorSubject<Exercise[]>;
  expertSolutions: BehaviorSubject<ExpertSolution[]>;
  exercisesFetched: Boolean = false;

  constructor(private http: HttpClient) {
    this.exercises = new BehaviorSubject<Exercise[]>([]);
    this.expertSolutions = new BehaviorSubject<ExpertSolution[]>([]);
    this.fetchExercises();
  }

  postExpertSolutionFile(fileToUpload: File): Observable<any> {
    const formData: FormData = new FormData();

    formData.append('file', fileToUpload, fileToUpload.name);
    return this.http.post('http://127.0.0.1:3001/expertsolution/register', formData);
  }

  getExpertSolutions(): BehaviorSubject<ExpertSolution[]> {
    if (!this.exercisesFetched) this.fetchExercises();

    return this.expertSolutions;
  }

  getExercises(): BehaviorSubject<Exercise[]> {
    if (!this.exercisesFetched) this.fetchExercises();

    return this.exercises;
  }

  getExercise(exerciseId: string): Observable<Exercise> {
    let exercise$: Observable<Exercise> = new Observable((sub) => {
      this.getExercises().subscribe((exercises: Exercise[]) => {
          sub.next(
            exercises
              .filter((ex: Exercise) => ex.exercise_id === exerciseId)
              .pop()
          );
      });
    });
    return exercise$;
  }

  getExpertSolution(expertSolutionId: string): Observable<ExpertSolution> {
    let expertSolution$: Observable<ExpertSolution> = new Observable((sub) => {
      this.getExpertSolutions()
        .subscribe((expertSolutions: ExpertSolution[]) => {
          sub.next(
            expertSolutions
              .filter((ex) => ex.expert_solution_id === expertSolutionId)
              .pop()
          );
        });
    });
    return expertSolution$;
  }

  fetchExercises(): void {
    this.exercisesFetched = true;

    this.http
      .get('http://localhost:3001/exercise')
      .subscribe((result: Exercise[]) => {
        let _expertSolutions: ExpertSolution[] = new Array<ExpertSolution>();
        for (let exercise of result) {
          _expertSolutions.push(...exercise.expert_solutions);
        }
        this.expertSolutions.next(_expertSolutions);

        return this.exercises.next(result)});
  }
}
