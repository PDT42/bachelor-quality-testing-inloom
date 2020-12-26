import { Evaluation } from './evaluation';

export interface TestDataSet {
  test_data_set_id: string;
  exercise_id: string;
  expert_solution_id: string;
  student_id: string;
  meta_model_type: string;
  max_points: number;
  auto_evals: Evaluation[];
  man_evals: Evaluation[];
}
