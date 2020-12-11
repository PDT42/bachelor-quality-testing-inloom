import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {DashboardComponent} from "./dashboard/dashboard.component";
import { ListtestdatasetsComponent } from './listtestdatasets/listtestdatasets.component';
import {RegisterAutoEval} from "./register-auto-eval/register-auto-eval.component";

const routes: Routes = [
  {path: '', component: DashboardComponent},
  {path: 'eval/auto/upload', component: RegisterAutoEval},
  {path: 'eval/man/upload', component: RegisterAutoEval},
  {path: 'testdatasets', component: ListtestdatasetsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
