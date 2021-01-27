import {
  Component,
  ComponentFactoryResolver,
  OnInit,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { ExerciseService } from 'src/app/services/exercise.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';
import { TestDataSet } from '../../classes/test-data-set';
import { TestDataSetService } from '../../services/test-data-set-service.service';
import { SingleComparisonComponent } from '../single-comparison/single-comparison.component';
import { TdsComparisonComponent } from '../tds-comparison/tds-comparison.component';

@Component({
  selector: 'app-test-data-set-details',
  templateUrl: './test-data-set-details.component.html',
  styleUrls: ['./test-data-set-details.component.css'],
})
export class TestDataSetDetailsComponent implements OnInit {
  testDataSetId: string;
  advancedComparisonForm: FormGroup;

  @ViewChild('comparisonRoot', { read: ViewContainerRef })
  viewContainerRef: ViewContainerRef;

  constructor(
    private _formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    public tdsService: TestDataSetService,
    public metaEvalService: MetaEvalService,
    public exerciseService: ExerciseService,
    public evaluationService: EvaluationService,
    private componentFactoryResolver: ComponentFactoryResolver
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.testDataSetId = params['id'];
    });
    this.advancedComparisonForm = this._formBuilder.group({
      manEvalSelectionCtrl: ['', Validators.required],
      autoEvalSelectionCtrl: ['', Validators.required],
    });
  }

  getTestDataSetTitle(): Observable<string> {
    let testDataSetTitle$: Observable<string> = new Observable((sub) => {
      this.tdsService
        .getTestDataSet(this.testDataSetId)
        .subscribe((testDataSet: TestDataSet) => {
          if (testDataSet) {
            sub.next(
              'TDS - Exercise: ' +
                testDataSet.exercise_id +
                ' - Student: ' +
                testDataSet.student_id
            );
          }
        });
    });
    return testDataSetTitle$;
  }

  deleteTDS(): void {
    this.tdsService.deleteTDS(this.testDataSetId);
    this.router.navigate(['register']);
  }

  onSelectionSubmit(event: any): void {
    const factory = this.componentFactoryResolver.resolveComponentFactory(
      TdsComparisonComponent
    );
    this.viewContainerRef.clear();
    const component = this.viewContainerRef.createComponent(factory);
    component.instance.testDataSetId = this.testDataSetId;
    component.instance.manEvalKey = this.advancedComparisonForm.get(
      'manEvalSelectionCtrl'
    ).value;
    component.instance.autoEvalKey = this.advancedComparisonForm.get(
      'autoEvalSelectionCtrl'
    ).value;
  }
}
