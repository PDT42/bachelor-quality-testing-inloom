import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { FileUploadService } from '../../services/file-upload.service';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-file-upload',
  templateUrl: './register-auto-eval.component.html',
  styleUrls: ['./register-auto-eval.component.css'],
})
export class RegisterAutoEval implements OnInit {
  fileForm: FormGroup;
  fileToUpload: File = null;
  testDataSetId: string;

  constructor(
    private fileUploadService: FileUploadService,
    private testDataSetService: TestDataSetService,
    private _formBuilder: FormBuilder,
    private evalService: EvaluationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.fileForm = this._formBuilder.group({
      fileCtrl: [null],
    });
  }

  handleFileInput(file: File): void {
    this.fileToUpload = file;
  }

  uploadFile(): void {
    this.fileUploadService.postAutoEvalFile(this.fileToUpload)
    .subscribe((result: any) => {
      this.testDataSetService.fetchData();
      this.evalService.fetchEvaluations();
      this.router.navigate(['/register']);
      return result;
    });
  }
}
