import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Evaluator } from 'src/app/classes/evaluator';
import { EvaluatorService } from 'src/app/services/evaluator.service';

@Component({
  selector: 'app-register-evaluator',
  templateUrl: './register-evaluator.component.html',
  styleUrls: ['./register-evaluator.component.css'],
})
export class RegisterEvaluatorComponent implements OnInit {
  evaluatorForm: FormGroup;

  constructor(
    private _formBuilder: FormBuilder,
    private evaluatorService: EvaluatorService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.evaluatorForm = this._formBuilder.group({
      firstnameCtrl: ['', Validators.required],
      lastnameCtrl: ['', Validators.required],
    });
  }

  onSubmit(): void {
    let evaluator: Evaluator = new Evaluator();
    evaluator.first_name = this.evaluatorForm.get('firstnameCtrl').value;
    evaluator.last_name = this.evaluatorForm.get('lastnameCtrl').value;

    this.evaluatorService.registerEvaluator(evaluator);
    this.router.navigate(['/register']);
  }
}
