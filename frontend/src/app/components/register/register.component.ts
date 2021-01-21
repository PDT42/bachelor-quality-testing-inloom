import { Component, OnInit } from '@angular/core';
import { TestDataSetService } from 'src/app/services/test-data-set-service.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  constructor(
    public tdsService: TestDataSetService
  ) { }

  ngOnInit(): void {
  }

}
