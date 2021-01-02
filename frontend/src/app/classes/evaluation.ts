import { Timestamp } from 'rxjs';
import { Result } from './result';

export class Evaluation {
  exercise_id: string;
  expert_solution_id: string;
  student_id: string;
  evaluation_type: string;
  test_data_set_id: string;
  total_points: number;
  results: Array<Result>;
  evaluation_id: string;
  created_time: number;
  mcs_identifier: string;
  mcs_version: string;
  evaluator_id: string;
}
