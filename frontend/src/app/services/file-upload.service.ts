import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// TODO: Move this to evaluation service

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {
  constructor(private http: HttpClient) {}

  postAutoEvalFile(fileToUpload: File): Observable<any> {
    const formData: FormData = new FormData();

    formData.append('file', fileToUpload, fileToUpload.name);
    return this.http.post('http://127.0.0.1:3001/eval/register/auto', formData);
  }
}
