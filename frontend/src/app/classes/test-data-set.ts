import { Evaluation } from './evaluation';

export interface TestDataSet {
  exercise_id: string;
  expert_solution_id: string;
  student_id: string;
  auto_evals: Evaluation[];
  man_evals: Evaluation[];
  test_data_set_id: string;
  created_time: number;
}
