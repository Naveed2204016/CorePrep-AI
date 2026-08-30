export type RoadmapMode = "topic" | "job";

export interface RoadmapResource {
  title: string;
  url: string;
  type: string;
}

export interface RoadmapTopic {
  id: string | number;
  title: string;
  dayRange: string;
  description: string;
  resources: RoadmapResource[];
  completed?: boolean;
}

export interface GeneratedRoadmap {
  id: string | number;
  title: string;
  mode: RoadmapMode;
  weeks: number;
  sourceLabel: string;
  topics: RoadmapTopic[];
  confirmed: boolean;
  editNote?: string;
  createdAt?: string;
  generationSource?: "qwen-rag" | "fallback";
}

export interface RoadmapInput {
  mode: RoadmapMode;
  weeks: number;
  topic?: string;
  jobFileName?: string;
  jobFile?: File;
}

export interface AssessmentConfig {
  topicId: string | number;
  mcqCount: number;
  shortCount: number;
  durationMinutes: number;
}

export interface AssessmentQuestion {
  id: number;
  type: "mcq" | "short";
  question: string;
  options?: string[] | null;
}

export interface GeneratedAssessment {
  assessmentId: number;
  topicId: number;
  durationMinutes: number;
  questions: AssessmentQuestion[];
  generationSource: "groq-rag";
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
  topicId: string | number;
  score: number;
  correctCount: number;
  totalQuestions: number;
  passed: boolean;
  revisionAreas: string[];
  items: ExamResultItem[];
  evaluationSource?: "groq-rag" | "fallback" | "stored";
}
