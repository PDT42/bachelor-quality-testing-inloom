import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {
  constructor(private http: HttpClient) {}

  postAutoEvalFile(fileToUpload: File): void {
    const formData: FormData = new FormData();

    formData.append('file', fileToUpload, fileToUpload.name);
    this.http
      .post('http://127.0.0.1:3001/eval/auto/upload', formData)
      .subscribe((result) => {
        return result;
      });
  }
}
