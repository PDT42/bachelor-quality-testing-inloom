import { ExpertElement } from "./expert-element";

export class ExpertSolution {
  expert_solution_id: string;
  exercise_id: string;
  maximum_points: number;
  elements: Map<string, ExpertElement[]>;
  created_time: number;
}
