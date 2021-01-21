import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { v4 as uuidv4 } from 'uuid';
import { ExpertElement } from 'src/app/classes/expert-element';
import { ExpertSolution } from 'src/app/classes/expert-solution';
import { ExerciseService } from 'src/app/services/exercise.service';
import { TestDataSetService } from 'src/app/services/test-data-set-service.service';
import { Evaluation } from '../../classes/evaluation';
import { Result } from '../../classes/result';
import { EvaluationService } from '../../services/evaluation.service';
import { EvaluatorService } from '../../services/evaluator.service';

@Component({
  selector: 'app-register-man-eval',
  templateUrl: './register-man-eval.component.html',
  styleUrls: ['./register-man-eval.component.css'],
})
export class RegisterManEvalComponent implements OnInit {
  fileForm: FormGroup;
  evalIdentForm: FormGroup;
  metadataForm: FormGroup;
  resultsForm: FormGroup;
  evalFile: File;
  results: Result[];
  total_points: number = 0.0;
  result_points_added: number = 0.0;
  expert_solutions: ExpertSolution[] = [];
  expert_elements: Object = new Object();
  type_elements: ExpertElement[] = [];

  result_category_colors = {
    M: '#6e1212',
    E: '#c71c10',
    W: '#ebda46',
    C: '#358f17',
    I: '#3b87a1',
  };

  constructor(
    private _formBuilder: FormBuilder,
    private evalService: EvaluationService,
    private tdsService: TestDataSetService,
    public exerciseService: ExerciseService,
    public evaluatorService: EvaluatorService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.fileForm = this._formBuilder.group({
      fileCtrl: [null],
    });
    this.evalIdentForm = this._formBuilder.group({
      exerciseIdCtrl: ['', Validators.required],
      studentIdCtrl: ['', Validators.required],
      expertSolIdCtrl: ['', Validators.required],
    });
    this.metadataForm = this._formBuilder.group({
      evaluatorIdCtrl: ['', Validators.required],
      totalPointsCtrl: ['', Validators.required],
    });
    this.resultsForm = this._formBuilder.group({
      expElCtrl: ['', Validators.required],
      expTypeCtrl: ['', Validators.required],
      stdElCtrl: ['', Validators.required],
      stdTypeCtrl: ['', Validators.required],
      featureCtrl: [null],
      resCatCtrl: ['', Validators.required],
      pointsCtrl: ['', Validators.required],
      feedbackCtrl: [''],
    });
    this.results = [];
  }

  fileChanged(file: File): void {
    let fileReader = new FileReader();

    if (file) {
      fileReader.onload = (e: any) => {
        this.fileForm.patchValue({ fileCtrl: fileReader.result });
        this.evalFile = e.target.result;
      };

      fileReader.readAsArrayBuffer(file);
    }
  }

  exerciseChanged(): void {
    this.expert_solutions = [];
    this.exerciseService.getExercises().subscribe((result) => {
      for (let index: number = 0; index < result.length; index++) {
        if (
          result[index].exercise_id ===
          this.evalIdentForm.get('exerciseIdCtrl').value
        ) {
          this.expert_solutions = this.expert_solutions.concat(
            result[index].expert_solutions
          );
        }
      }
    });
  }

  expertSolutionChanged(): void {
    let expert_sol_id = this.evalIdentForm.get('expertSolIdCtrl').value;
    this.expert_elements = this.expert_solutions
      .filter((e) => e.expert_solution_id === expert_sol_id)
      .pop().elements;
  }

  expertLabelChanged(event: any): void {
    this.resultsForm
      .get('stdElCtrl')
      .setValue(event.element_label);
  }

  totalPointsChanged(): void {
    this.total_points = this.metadataForm.get('totalPointsCtrl').value;
  }

  expertTypeChanged(event: any): void {
    let selected_type = this.resultsForm.get('expTypeCtrl').value;
    this.type_elements = this.expert_elements[selected_type];
    this.resultsForm.get('stdTypeCtrl')
    .setValue(event.value);
  }

  addResult() {
    let new_result: Result = {
      expert_element: this.resultsForm.get('expElCtrl').value,
      student_element_type: this.resultsForm.get('stdTypeCtrl').value,
      student_element_label: this.resultsForm.get('stdElCtrl').value,
      graded_feature_id: this.resultsForm.get('featureCtrl').value,
      result_category: this.resultsForm.get('resCatCtrl').value,
      points: Number(this.resultsForm.get('pointsCtrl').value),
      feedback_message: this.resultsForm.get('feedbackCtrl').value,
      result_type: 'MANUAL',
      evaluation_id: null,
      result_id: uuidv4(),
    };

    if (!this.total_points) {
      this.total_points = this.metadataForm.get('total_points').value;
    }

    this.result_points_added += new_result.points;
    this.results.push(new_result);

    this.resultsForm.reset();
  }

  removeResult(result: Result): void {
    let _index = this.results.indexOf(result);
    if (_index > -1) {
      this.results.splice(_index, 1);
    }
    this.total_points -= result.points;
  }

  onSubmit() {
    let manEval: Evaluation = {
      exercise_id: this.evalIdentForm.get('exerciseIdCtrl').value,
      expert_solution_id: this.evalIdentForm.get('expertSolIdCtrl').value,
      student_id: this.evalIdentForm.get('studentIdCtrl').value,
      evaluation_type: 'M',
      total_points: this.metadataForm.get('totalPointsCtrl').value,
      results: this.results,
      mcs_identifier: null,
      mcs_version: null,
      evaluator_id: this.metadataForm.get('evaluatorIdCtrl').value,
      evaluation_id: null,
      test_data_set_id: null,
      created_time: null,
    };

    this.evalService.registerEvaluation(manEval);
    this.router.navigate(['/register']);
  }
}
