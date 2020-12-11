import { Evaluation } from './evaluation';

export interface TestDataSet {
  expert_model_id: string;
  student_model_id: string;
  meta_model_type: string;
  mcs_identifier: string;
  mcs_version: string;
  auto_eval_id: string;
  man_eval_id: string;
  auto_eval: Evaluation
  man_eval: Evaluation
}
