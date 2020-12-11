import { ConstraintResult } from './constraint-result';

export interface Evaluation {
  type: string;
  evaluator: string;
  student_model_id: string;
  expert_model_id: string;
  total_points: number;
  max_points: number;
  results: Array<ConstraintResult>;
  evaluation_id: string;
}
