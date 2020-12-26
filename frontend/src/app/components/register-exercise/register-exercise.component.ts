import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ExerciseService } from 'src/app/services/exercise.service';

@Component({
  selector: 'app-register-exercise',
  templateUrl: './register-exercise.component.html',
  styleUrls: ['./register-exercise.component.css']
})
export class RegisterExerciseComponent implements OnInit {
  fileForm: FormGroup
  fileToUpload: File = null;
  testDataSet: string;

  constructor(
    private exerciseService: ExerciseService,
    private _formBuilder: FormBuilder,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.fileForm = this._formBuilder.group({
      fileCtrl: [null]
    });
  }


  handleFileInput(file: File): void {
    this.fileToUpload = file;
  }

  uploadFile(): void {
    this.exerciseService.postExpertSolutionFile(this.fileToUpload)
    .subscribe((result: any) => {
      this.exerciseService.fetchExercises();
      this.router.navigate(['/register']);
      return result;
    });
  }
}
