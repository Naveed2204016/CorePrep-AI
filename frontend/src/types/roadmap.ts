export type RoadmapMode = "topic" | "job";

export interface RoadmapResource {
  title: string;
  url: string;
  type: string;
}

export interface RoadmapTopic {
  id: string;
  title: string;
  dayRange: string;
  description: string;
  resources: RoadmapResource[];
}

export interface GeneratedRoadmap {
  id: string;
  title: string;
  mode: RoadmapMode;
  weeks: number;
  sourceLabel: string;
  topics: RoadmapTopic[];
  confirmed: boolean;
  editNote?: string;
}

export interface RoadmapInput {
  mode: RoadmapMode;
  weeks: number;
  topic?: string;
  jobFileName?: string;
}

export interface AssessmentConfig {
  topicId: string;
  mcqCount: number;
  shortCount: number;
  durationMinutes: number;
}

export interface MCQQuestion {
  id: string;
  type: "mcq";
  question: string;
  options: string[];
  correctAnswer: string;
  explanation: string;
  revisionArea: string;
}

export interface ShortQuestion {
  id: string;
  type: "short";
  question: string;
  referenceAnswer: string;
  explanation: string;
  revisionArea: string;
}

export type ExamQuestion = MCQQuestion | ShortQuestion;

export interface ExamResultItem {
  questionId: string;
  type: "mcq" | "short";
  question: string;
  userAnswer: string;
  correctAnswer: string;
  explanation: string;
  correct: boolean;
  revisionArea: string;
}

export interface ExamResult {
  topicId: string;
  score: number;
  correctCount: number;
  totalQuestions: number;
  passed: boolean;
  revisionAreas: string[];
  items: ExamResultItem[];
}