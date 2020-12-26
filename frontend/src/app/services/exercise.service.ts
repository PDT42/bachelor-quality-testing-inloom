import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Exercise } from '../classes/exercise';

@Injectable({
  providedIn: 'root',
})
export class ExerciseService {
  exercises: BehaviorSubject<Exercise[]>;
  exercisesFetched: Boolean = false;

  constructor(private http: HttpClient) {
    this.exercises = new BehaviorSubject<Exercise[]>([]);
    this.fetchExercises();
  }

  postExpertSolutionFile(fileToUpload: File): Observable<any> {
    const formData: FormData = new FormData();

    formData.append('file', fileToUpload, fileToUpload.name);
    return this.http.post('http://127.0.0.1:3001/expertsolution/register', formData);
  }

  getExercises(): BehaviorSubject<Exercise[]> {
    if (!this.exercisesFetched) this.fetchExercises();

    return this.exercises;
  }

  fetchExercises(): void {
    this.exercisesFetched = true;

    this.http
      .get('http://localhost:3001/exercise')
      .subscribe((result: Exercise[]) => this.exercises.next(result));
  }
}
