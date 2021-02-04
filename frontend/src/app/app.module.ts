import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from '@angular/material/slider';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatStepperModule } from '@angular/material/stepper';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDividerModule } from '@angular/material/divider';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatTabsModule } from '@angular/material/tabs';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule } from '@angular/forms';

import { PdfViewerModule } from 'ng2-pdf-viewer';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ListTestTataSetsComponent } from './components/list-test-data-sets/list-test-data-sets.component';
import { RegisterAutoEval } from './components/register-auto-eval/register-auto-eval.component';
import { RegisterManEvalComponent } from './components/register-man-eval/register-man-eval.component';
import { EvaluationDetailsComponent } from './components/evaluation-details/evaluation-details.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { RegisterComponent } from './components/register/register.component';
import { TestDataSetDetailsComponent } from './components/test-data-set-details/test-data-set-details.component';
import { ListEvaluationsComponent } from './components/list-evaluations/list-evaluations.component';
import { RegisterExerciseComponent } from './components/register-exercise/register-exercise.component';
import { ListEvaluatorsComponent } from './components/list-evaluators/list-evaluators.component';
import { ListExercisesComponent } from './components/list-exercises/list-exercises.component';
import { ExerciseDetailsComponent } from './components/exercise-details/exercise-details.component';
import { EvaluatorDetailsComponent } from './components/evaluator-details/evaluator-details.component';
import { RegisterEvaluatorComponent } from './components/register-evaluator/register-evaluator.component';
import { SingleComparisonComponent } from './components/single-comparison/single-comparison.component';
import { MultipleComparisonComponent } from './components/multiple-comparison/multiple-comparison.component';
import { TdsComparisonComponent } from './components/tds-comparison/tds-comparison.component';
import { CategoryByElementComponent } from './components/category-by-element/category-by-element.component';
import { BackButtonComponent } from './components/back-button/back-button.component';
import { ExerciseLevelComparisonComponent } from './components/exercise-level-comparison/exercise-level-comparison.component';
import { AbsolutePipe } from './pipes/absolute.pipe';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    RegisterAutoEval,
    ListTestTataSetsComponent,
    EvaluationDetailsComponent,
    RegisterManEvalComponent,
    NavigationComponent,
    RegisterComponent,
    TestDataSetDetailsComponent,
    ListEvaluationsComponent,
    RegisterExerciseComponent,
    ListEvaluatorsComponent,
    ListExercisesComponent,
    ExerciseDetailsComponent,
    EvaluatorDetailsComponent,
    RegisterEvaluatorComponent,
    SingleComparisonComponent,
    MultipleComparisonComponent,
    TdsComparisonComponent,
    CategoryByElementComponent,
    BackButtonComponent,
    ExerciseLevelComparisonComponent,
    AbsolutePipe,
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatSliderModule,
    MatToolbarModule,
    MatIconModule,
    MatCardModule,
    MatButtonToggleModule,
    MatStepperModule,
    MatGridListModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDividerModule,
    MatSelectModule,
    MatTabsModule,
    MatProgressSpinnerModule,
    PdfViewerModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
