import { ExpertElement } from "./expert-element";

export interface Result {
  evaluation_id: string;
  expert_element: ExpertElement;
  student_element_label: string;
  student_element_type: string;
  result_category: string;
  points: number;
  feedback_message: string;
  result_type: string;
  graded_feature_id: string;
  result_id: string;
}
