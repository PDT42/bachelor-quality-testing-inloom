import { Component, OnInit } from '@angular/core';
import {FileUploadService} from "../services/file-upload.service";

@Component({
  selector: 'app-file-upload',
  templateUrl: './register-auto-eval.component.html',
  styleUrls: ['./register-auto-eval.component.css']
})
export class RegisterAutoEval implements OnInit {

  fileToUpload: File = null;

  constructor(private fileUploadService: FileUploadService) { }

  handleFileInput(files: FileList): void {
    this.fileToUpload = files.item(0)
  }

  uploadFile(): void {
    this.fileUploadService.postAutoEvalFile(this.fileToUpload)
  }

  ngOnInit(): void {
  }
}
