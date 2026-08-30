import type {
  AssessmentConfig,
  ExamQuestion,
  ExamResult,
  GeneratedAssessment,
  GeneratedRoadmap,
  RoadmapInput,
} from "../types/roadmap";

export const SUPPORTED_TOPICS = [
  "Data Structures & Algorithms",
  "Object-Oriented Programming",
  "DBMS",
  "Operating Systems",
  "Computer Networks",
  "System Design",
  "Frontend Development",
  "Backend Development",
  "Machine Learning",
  "DevOps",
  "Git & GitHub",
  "Software Testing & QA",
];

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const apiRequest = async <T>(path: string, init: RequestInit = {}): Promise<T> => {
  const token = localStorage.getItem("coreprep_token");
  const isFormData = init.body instanceof FormData;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(!isFormData ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "The roadmap request failed");
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json();
};

const cacheCurrentRoadmap = (roadmap: GeneratedRoadmap) => {
  sessionStorage.setItem("coreprep_roadmap", JSON.stringify(roadmap));
};

/* The backend owns curriculum generation and resource selection. */
/*
const topicUnits: Record<string, string[]> = {
  "Data Structures & Algorithms": [
    "Complexity, Arrays & Strings",
    "Linked Lists, Stacks & Queues",
    "Trees & Binary Search Trees",
    "Graphs & Traversal",
    "Sorting, Searching & Dynamic Programming",
  ],

  "Object-Oriented Programming": [
    "OOP Fundamentals",
    "Encapsulation & Abstraction",
    "Inheritance & Polymorphism",
    "SOLID Principles",
    "Common OOP Interview Scenarios",
  ],

  DBMS: [
    "Database Fundamentals & ER Model",
    "SQL, Joins & Queries",
    "Normalization",
    "Transactions & ACID",
    "Indexing & Concurrency",
  ],

  "Operating Systems": [
    "Processes & Threads",
    "CPU Scheduling",
    "Synchronization",
    "Deadlocks",
    "Memory & Virtual Memory",
  ],

  "Computer Networks": [
    "OSI & TCP/IP",
    "IP Addressing",
    "TCP vs UDP",
    "HTTP, DNS & Web Communication",
    "Routing & Network Security Basics",
  ],

  "System Design": [
    "System Design Fundamentals",
    "Caching & Load Balancing",
    "Database Scaling",
    "Queues & Asynchronous Systems",
    "Scalability & Reliability",
  ],

  "Frontend Development": [
    "HTML, CSS & Browser Fundamentals",
    "JavaScript Fundamentals",
    "TypeScript",
    "React Fundamentals",
    "Frontend Performance & Architecture",
  ],

  "Backend Development": [
    "Backend & API Fundamentals",
    "REST APIs",
    "Authentication & Authorization",
    "Databases & Backend Integration",
    "Scalability & API Security",
  ],

  "Machine Learning": [
    "ML Fundamentals",
    "Supervised vs Unsupervised Learning",
    "Model Evaluation",
    "Overfitting & Regularization",
    "Common ML Interview Concepts",
  ],

  DevOps: [
    "DevOps Fundamentals",
    "Linux & Shell Basics",
    "Docker",
    "CI/CD",
    "Deployment & Monitoring",
  ],

  "Git & GitHub": [
    "Git Fundamentals",
    "Branches & Merging",
    "Remote Repositories",
    "Pull Requests & Collaboration",
    "Common Git Interview Scenarios",
  ],

  "Software Testing & QA": [
    "Testing Fundamentals",
    "Unit & Integration Testing",
    "Black-box & White-box Testing",
    "Test Cases & Quality Assurance",
    "Automation & CI Testing",
  ],
};

const resourceMap: Record<string, { title: string; url: string }> = {
  "Data Structures & Algorithms": {
    title: "DSA Learning Resource",
    url: "https://www.geeksforgeeks.org/data-structures/",
  },

  "Object-Oriented Programming": {
    title: "OOP Learning Resource",
    url: "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/",
  },

  DBMS: {
    title: "DBMS Learning Resource",
    url: "https://www.geeksforgeeks.org/dbms/",
  },

  "Operating Systems": {
    title: "Operating Systems Resource",
    url: "https://www.geeksforgeeks.org/operating-systems/",
  },

  "Computer Networks": {
    title: "Computer Networks Resource",
    url: "https://www.geeksforgeeks.org/computer-network-tutorials/",
  },

  "System Design": {
    title: "System Design Resource",
    url: "https://www.geeksforgeeks.org/system-design-tutorial/",
  },

  "Frontend Development": {
    title: "MDN Web Documentation",
    url: "https://developer.mozilla.org/",
  },

  "Backend Development": {
    title: "FastAPI Documentation",
    url: "https://fastapi.tiangolo.com/",
  },

  "Machine Learning": {
    title: "Machine Learning Resource",
    url: "https://www.geeksforgeeks.org/machine-learning/",
  },

  DevOps: {
    title: "Docker Documentation",
    url: "https://docs.docker.com/",
  },

  "Git & GitHub": {
    title: "Git Documentation",
    url: "https://git-scm.com/doc",
  },

  "Software Testing & QA": {
    title: "Software Testing Resource",
    url: "https://www.geeksforgeeks.org/software-testing/",
  },
};

const wait = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms));

const createDayRanges = (weeks: number, count: number) => {
  const totalDays = weeks * 7;
  const block = Math.floor(totalDays / count);

  return Array.from({ length: count }, (_, index) => {
    const start = index * block + 1;

    const end =
      index === count - 1
        ? totalDays
        : Math.min((index + 1) * block, totalDays);

    return `Day ${start}-${end}`;
  });
};

const createTopicRoadmap = (
  subject: string,
  weeks: number
): RoadmapTopic[] => {
  const units = topicUnits[subject] ?? [
    `${subject} Fundamentals`,
    `${subject} Core Concepts`,
    `${subject} Intermediate Topics`,
    `${subject} Interview Questions`,
    `${subject} Revision`,
  ];

  const ranges = createDayRanges(weeks, units.length);

  const resource =
    resourceMap[subject] ??
    resourceMap["Data Structures & Algorithms"];

  return units.map((unit, index) => ({
    id: `topic-${index + 1}`,
    title: unit,
    dayRange: ranges[index],
    description: `Study the important interview concepts of ${unit}, review examples and prepare for the required assessment.`,
    resources: [
      {
        title: resource.title,
        url: resource.url,
        type: "Learning Resource",
      },
      {
        title: "Interview Practice",
        url: "https://www.geeksforgeeks.org/",
        type: "Practice",
      },
    ],
  }));
};

const createJobRoadmap = (weeks: number): RoadmapTopic[] => {
  const units = [
    {
      title: "Programming & Problem Solving",
      url: "https://www.geeksforgeeks.org/data-structures/",
    },
    {
      title: "Frontend Fundamentals",
      url: "https://developer.mozilla.org/",
    },
    {
      title: "Backend & REST APIs",
      url: "https://fastapi.tiangolo.com/",
    },
    {
      title: "Database Fundamentals",
      url: "https://www.geeksforgeeks.org/dbms/",
    },
    {
      title: "Git, Development Workflow & Testing",
      url: "https://git-scm.com/doc",
    },
    {
      title: "System Design Fundamentals",
      url: "https://www.geeksforgeeks.org/system-design-tutorial/",
    },
  ];

  const ranges = createDayRanges(weeks, units.length);

  return units.map((unit, index) => ({
    id: `topic-${index + 1}`,
    title: unit.title,
    dayRange: ranges[index],
    description:
      "Review the concepts detected as important for the target software engineering role and complete the assessment before moving forward.",
    resources: [
      {
        title: `${unit.title} Resource`,
        url: unit.url,
        type: "Recommended",
      },
    ],
  }));
};
*/

export const roadmapService = {
  async generateRoadmap(
    input: RoadmapInput
  ): Promise<GeneratedRoadmap> {
    let roadmap: GeneratedRoadmap;
    if (input.mode === "job") {
      if (!input.jobFile) throw new Error("Please upload a job description first.");
      const form = new FormData();
      form.append("timeline", String(input.weeks));
      form.append("file", input.jobFile);
      roadmap = await apiRequest<GeneratedRoadmap>("/roadmaps/generate-from-job", {
        method: "POST",
        body: form,
      });
    } else {
      roadmap = await apiRequest<GeneratedRoadmap>("/roadmaps/generate", {
        method: "POST",
        body: JSON.stringify({ subject: input.topic, timeline: input.weeks }),
      });
    }
    cacheCurrentRoadmap(roadmap);
    return roadmap;
  },

  async suggestEdit(roadmapId: string | number, suggestion: string) {
    const roadmap = await apiRequest<GeneratedRoadmap>(
      `/roadmaps/${roadmapId}/suggest-edit`,
      { method: "POST", body: JSON.stringify({ suggestion }) },
    );
    cacheCurrentRoadmap(roadmap);
    return roadmap;
  },

  async confirmRoadmap(roadmapId: string | number) {
    const roadmap = await apiRequest<GeneratedRoadmap>(
      `/roadmaps/${roadmapId}/confirm`,
      { method: "POST" },
    );
    cacheCurrentRoadmap(roadmap);
    const cached = this.getRoadmaps().filter((item) => item.id !== roadmap.id);
    localStorage.setItem("coreprep_roadmaps", JSON.stringify([roadmap, ...cached]));
    return roadmap;
  },

  async fetchRoadmaps() {
    const roadmaps = await apiRequest<GeneratedRoadmap[]>("/roadmaps");
    localStorage.setItem("coreprep_roadmaps", JSON.stringify(roadmaps));
    return roadmaps;
  },

  async deleteRoadmap(roadmapId: string | number) {
    await apiRequest<void>(`/roadmaps/${roadmapId}`, { method: "DELETE" });

    const target = this.getRoadmaps().find((item) => item.id === roadmapId);
    const remaining = this.getRoadmaps().filter((item) => item.id !== roadmapId);
    localStorage.setItem("coreprep_roadmaps", JSON.stringify(remaining));

    const current = this.getRoadmap();
    if (current?.id === roadmapId) {
      sessionStorage.removeItem("coreprep_roadmap");
    }

    if (target) {
      const removedTopicIds = new Set(target.topics.map((topic) => String(topic.id)));
      const completed = this.getCompletedTopics().filter(
        (topicId) => !removedTopicIds.has(topicId),
      );
      localStorage.setItem("coreprep_completed_topics", JSON.stringify(completed));
    }
  },

  async generateAssessment(
    roadmapId: string | number,
    topicId: string | number,
    mcqCount: number,
    shortCount: number,
    durationMinutes: number,
  ) {
    const assessment = await apiRequest<GeneratedAssessment>("/assessments/generate", {
      method: "POST",
      body: JSON.stringify({
        roadmap_id: Number(roadmapId),
        topic_id: Number(topicId),
        num_mcq: mcqCount,
        num_short: shortCount,
        duration_minutes: durationMinutes,
      }),
    });
    sessionStorage.setItem("coreprep_active_assessment", JSON.stringify(assessment));
    sessionStorage.setItem(
      "coreprep_assessment_deadline",
      String(Date.now() + assessment.durationMinutes * 60_000),
    );
    return assessment;
  },

  getActiveAssessment(): GeneratedAssessment | null {
    const stored = sessionStorage.getItem("coreprep_active_assessment");
    return stored ? JSON.parse(stored) : null;
  },

  getAssessmentDeadline(): number | null {
    const stored = sessionStorage.getItem("coreprep_assessment_deadline");
    return stored ? Number(stored) : null;
  },

  async submitAssessment(
    assessmentId: number,
    answers: Record<string, string>,
  ) {
    const requestStarted = Date.now();
    const submit = () => apiRequest<ExamResult>(`/assessments/${assessmentId}/submit`, {
      method: "POST",
      body: JSON.stringify({
        answers: Object.entries(answers).map(([questionId, answer]) => ({
          question_id: Number(questionId),
          answer,
        })),
      }),
    });
    let result: ExamResult;
    try {
      result = await submit();
    } catch (cause) {
      // Retry only quick failures (for example a brief dropped connection). A
      // long-running timeout should not start another three-minute evaluation.
      if (Date.now() - requestStarted >= 15_000) throw cause;
      await new Promise((resolve) => window.setTimeout(resolve, 750));
      result = await submit();
    }
    if (result.passed) {
      this.markTopicCompleted(result.topicId);
    }
    sessionStorage.removeItem("coreprep_assessment_deadline");
    sessionStorage.removeItem("coreprep_active_assessment");
    sessionStorage.removeItem(`coreprep_exam_answers_${assessmentId}`);
    return result;
  },

  getRoadmap(): GeneratedRoadmap | null {
    const stored = sessionStorage.getItem("coreprep_roadmap");

    return stored ? JSON.parse(stored) : null;
  },

  getRoadmaps(): GeneratedRoadmap[] {
    const stored = localStorage.getItem("coreprep_roadmaps");
    const roadmaps: GeneratedRoadmap[] = stored
      ? JSON.parse(stored)
      : [];
    const current = this.getRoadmap();

    if (current && !roadmaps.some((item) => item.id === current.id)) {
      return [current, ...roadmaps];
    }

    return roadmaps;
  },

  selectRoadmap(roadmap: GeneratedRoadmap) {
    sessionStorage.setItem(
      "coreprep_roadmap",
      JSON.stringify(roadmap)
    );
  },

  saveRoadmap(roadmap: GeneratedRoadmap) {
    sessionStorage.setItem(
      "coreprep_roadmap",
      JSON.stringify(roadmap)
    );

    const roadmaps = this.getRoadmaps().map((item) =>
      item.id === roadmap.id ? roadmap : item
    );
    localStorage.setItem(
      "coreprep_roadmaps",
      JSON.stringify(roadmaps)
    );

  },

  saveAssessmentConfig(config: AssessmentConfig) {
    sessionStorage.setItem(
      "coreprep_exam_config",
      JSON.stringify(config)
    );
  },

  getAssessmentConfig(): AssessmentConfig | null {
    const stored = sessionStorage.getItem(
      "coreprep_exam_config"
    );

    return stored ? JSON.parse(stored) : null;
  },

  getCompletedTopics(): string[] {
    const stored = localStorage.getItem(
      "coreprep_completed_topics"
    );

    const completed: Array<string | number> = stored ? JSON.parse(stored) : [];
    return completed.map(String);
  },

  markTopicCompleted(topicId: string | number) {
    const completed = this.getCompletedTopics();
    const normalizedTopicId = String(topicId);

    if (!completed.includes(normalizedTopicId)) {
      completed.push(normalizedTopicId);
    }

    localStorage.setItem(
      "coreprep_completed_topics",
      JSON.stringify(completed)
    );

    const update = (roadmap: GeneratedRoadmap) => ({
      ...roadmap,
      topics: roadmap.topics.map((topic) =>
        String(topic.id) === normalizedTopicId
          ? { ...topic, completed: true }
          : topic,
      ),
    });
    const current = this.getRoadmap();
    if (current?.topics.some((topic) => String(topic.id) === normalizedTopicId)) {
      sessionStorage.setItem("coreprep_roadmap", JSON.stringify(update(current)));
    }
    const roadmaps = this.getRoadmaps().map((roadmap) =>
      roadmap.topics.some((topic) => String(topic.id) === normalizedTopicId)
        ? update(roadmap)
        : roadmap,
    );
    localStorage.setItem("coreprep_roadmaps", JSON.stringify(roadmaps));
  },

  generateQuestions(
    topicTitle: string,
    mcqCount: number,
    shortCount: number
  ): ExamQuestion[] {
    const mcqTemplates = [
      {
        question: `Which approach best demonstrates strong understanding of ${topicTitle}?`,
        options: [
          "Memorizing definitions only",
          "Explaining concepts, trade-offs and examples",
          "Ignoring practical applications",
          "Learning syntax without understanding",
        ],
        correctAnswer:
          "Explaining concepts, trade-offs and examples",
        explanation:
          "Interviewers generally expect conceptual understanding together with the ability to explain reasoning and practical examples.",
      },

      {
        question: `What should be your first priority while preparing ${topicTitle}?`,
        options: [
          "Understand the fundamentals",
          "Memorize random questions",
          "Skip difficult concepts",
          "Only read advanced material",
        ],
        correctAnswer: "Understand the fundamentals",
        explanation:
          "A solid understanding of fundamentals makes advanced interview questions easier to reason about.",
      },

      {
        question: `Which preparation method is most useful for ${topicTitle}?`,
        options: [
          "Concept review followed by practice",
          "Reading without practice",
          "Only watching videos",
          "Avoiding assessments",
        ],
        correctAnswer:
          "Concept review followed by practice",
        explanation:
          "Combining study with retrieval practice helps expose gaps in understanding.",
      },

      {
        question: `During an interview question on ${topicTitle}, what is most important?`,
        options: [
          "Explain your reasoning clearly",
          "Answer as quickly as possible",
          "Avoid discussing assumptions",
          "Use complex terminology",
        ],
        correctAnswer:
          "Explain your reasoning clearly",
        explanation:
          "Clear reasoning allows the interviewer to evaluate how you approach the problem.",
      },

      {
        question: `After finding a weak area in ${topicTitle}, what should you do?`,
        options: [
          "Revise and reassess",
          "Ignore it",
          "Change the subject",
          "Memorize one answer",
        ],
        correctAnswer: "Revise and reassess",
        explanation:
          "Targeted revision followed by reassessment helps verify whether the weakness has been resolved.",
      },
    ];

    const mcqs: ExamQuestion[] = Array.from(
      { length: mcqCount },
      (_, index) => {
        const template =
          mcqTemplates[index % mcqTemplates.length];

        return {
          id: `mcq-${index + 1}`,
          type: "mcq",
          question:
            index < mcqTemplates.length
              ? template.question
              : `${template.question} (Practice ${index + 1})`,
          options: template.options,
          correctAnswer: template.correctAnswer,
          explanation: template.explanation,
          revisionArea: topicTitle,
        };
      }
    );

    const shorts: ExamQuestion[] = Array.from(
      { length: shortCount },
      (_, index) => ({
        id: `short-${index + 1}`,
        type: "short",
        question:
          index % 2 === 0
            ? `Explain an important concept from ${topicTitle} with a practical example.`
            : `Describe one common interview challenge related to ${topicTitle} and how you would approach it.`,
        referenceAnswer: `A strong answer should correctly explain the relevant ${topicTitle} concept, describe why it matters and include a clear example or reasoning process.`,
        explanation:
          "The answer should demonstrate conceptual understanding rather than only memorized definitions.",
        revisionArea: topicTitle,
      })
    );

    return [...mcqs, ...shorts];
  },

  evaluateExam(
    topicId: string | number,
    questions: ExamQuestion[],
    answers: Record<string, string>
  ): ExamResult {
    const items = questions.map((question) => {
      const userAnswer = answers[question.id] ?? "";

      const correct =
        question.type === "mcq"
          ? userAnswer === question.correctAnswer
          : userAnswer.trim().length >= 20;

      return {
        questionId: question.id,
        type: question.type,
        question: question.question,
        userAnswer,
        correctAnswer:
          question.type === "mcq"
            ? question.correctAnswer
            : question.referenceAnswer,
        explanation: question.explanation,
        correct,
        revisionArea: question.revisionArea,
      };
    });

    const correctCount = items.filter(
      (item) => item.correct
    ).length;

    const score =
      items.length === 0
        ? 0
        : Math.round(
            (correctCount / items.length) * 100
          );

    const revisionAreas = Array.from(
      new Set(
        items
          .filter((item) => !item.correct)
          .map((item) => item.revisionArea)
      )
    );

    return {
      topicId,
      score,
      correctCount,
      totalQuestions: items.length,
      passed: score >= 60,
      revisionAreas,
      items,
    };
  },
};
