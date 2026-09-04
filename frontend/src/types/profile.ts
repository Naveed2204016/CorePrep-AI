export type SubjectStatus =
  | "weak"
  | "needs_attention"
  | "strong"
  | "not_enough_data";

export interface SubjectPerformance {
  subject: string;
  answered: number;
  correct: number;
  incorrect: number;
  accuracy: number;
  weakness_score: number;
  status: SubjectStatus;
}

export interface PerformanceSummary {
  total_answered: number;
  overall_accuracy: number;
  weak_subjects: string[];
  subjects: SubjectPerformance[];
}

