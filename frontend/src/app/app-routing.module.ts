import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterExerciseComponent } from './components/register-exercise/register-exercise.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { EvaluationDetailsComponent } from './components/evaluation-details/evaluation-details.component';
import { ListTestTataSetsComponent } from './components/list-test-data-sets/list-test-data-sets.component';
import { RegisterAutoEval } from './components/register-auto-eval/register-auto-eval.component';
import { RegisterManEvalComponent } from './components/register-man-eval/register-man-eval.component';
import { RegisterComponent } from './components/register/register.component';
import { TestDataSetDetailsComponent } from './components/test-data-set-details/test-data-set-details.component';
import { RegisterEvaluatorComponent } from './components/register-evaluator/register-evaluator.component';
import { ExerciseDetailsComponent } from './components/exercise-details/exercise-details.component';

const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'testdataset', component: TestDataSetDetailsComponent },
  { path: 'testdataset/list', component: ListTestTataSetsComponent },
  { path: 'exercise', component: ExerciseDetailsComponent },
  { path: 'exercise/register', component: RegisterExerciseComponent },
  { path: 'evaluator/register', component: RegisterEvaluatorComponent },
  { path: 'eval', component: EvaluationDetailsComponent },
  { path: 'eval/man/register', component: RegisterManEvalComponent },
  { path: 'eval/auto/register', component: RegisterAutoEval },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
