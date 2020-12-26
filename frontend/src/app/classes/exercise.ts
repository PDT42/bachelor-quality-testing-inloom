import { ExpertSolution } from "./expert-solution";

export class Exercise {
  exercise_id: string;
  year: number;
  semester: string;
  type: string;
  meta_model_type: string;
  expert_solutions: ExpertSolution[];
}
