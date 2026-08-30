import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import {
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  AlertTriangle,
  Clock3,
  LoaderCircle,
  Send,
} from "lucide-react";

import { roadmapService } from "../services/roadmapService";

const AssessmentExamPage = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const roadmap =
    roadmapService.getRoadmap();

  const config =
    roadmapService.getAssessmentConfig();

  const topic = roadmap?.topics.find(
    (item) => String(item.id) === topicId
  );

  const assessment = roadmapService.getActiveAssessment();
  const deadline = roadmapService.getAssessmentDeadline();
  const questions = assessment?.questions ?? [];

  const answerStorageKey = assessment
    ? `coreprep_exam_answers_${assessment.assessmentId}`
    : null;

  const [answers, setAnswers] = useState<
    Record<string, string>
  >(() => {
    if (!answerStorageKey) return {};
    try {
      const stored = sessionStorage.getItem(answerStorageKey);
      return stored ? JSON.parse(stored) : {};
    } catch {
      return {};
    }
  });

  const [secondsLeft, setSecondsLeft] =
    useState(
      deadline
        ? Math.max(0, Math.ceil((deadline - Date.now()) / 1000))
        : config
          ? config.durationMinutes * 60
          : 0
    );

  const submitted = useRef(false);
  const autoSubmitAttempted = useRef(false);
  const [evaluating, setEvaluating] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const submitExam = useCallback(async () => {
    if (
      submitted.current ||
      !topicId ||
      !assessment ||
      questions.length === 0
    ) {
      return;
    }

    submitted.current = true;
    setEvaluating(true);
    setSubmitError("");
    try {
      const result = await roadmapService.submitAssessment(
        assessment.assessmentId,
        answers,
      );
      sessionStorage.setItem("coreprep_exam_result", JSON.stringify(result));
      if (result.passed) {
        roadmapService.markTopicCompleted(topicId);
      }
      navigate(`/roadmap/assessment/${topicId}/result`);
    } catch (cause) {
      submitted.current = false;
      setEvaluating(false);
      setSubmitError(cause instanceof Error ? cause.message : "Evaluation failed. Please submit again.");
    }
  }, [
    assessment,
    answers,
    navigate,
    questions,
    topicId,
  ]);

  useEffect(() => {
    if (answerStorageKey) {
      sessionStorage.setItem(answerStorageKey, JSON.stringify(answers));
    }
  }, [answerStorageKey, answers]);

  useEffect(() => {
    if (!config) return;

    const interval = setInterval(() => {
      setSecondsLeft(
        deadline
          ? Math.max(0, Math.ceil((deadline - Date.now()) / 1000))
          : 0,
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [config, deadline]);

  useEffect(() => {
    if (
      secondsLeft === 0 &&
      config &&
      !submitted.current &&
      !autoSubmitAttempted.current
    ) {
      autoSubmitAttempted.current = true;
      void submitExam();
    }
  }, [
    secondsLeft,
    config,
    submitExam,
  ]);

  if (
    !roadmap ||
    !config ||
    !assessment ||
    !topic ||
    !topicId
  ) {
    return (
      <main className="assessment-missing">
        <h1>No active exam found</h1>

        <Link
          to="/roadmap/current"
          className="primary-button"
        >
          Return to Roadmap
        </Link>
      </main>
    );
  }

  if (evaluating) {
    return (
      <main className="assessment-evaluation-loading">
        <LoaderCircle size={42} />
        <span>AI EVALUATION IN PROGRESS</span>
        <h1>Evaluating your answers</h1>
        <p>Groq is checking every response against the {roadmap.sourceLabel} corpus. This should finish within three minutes.</p>
      </main>
    );
  }

  const minutes = Math.floor(
    secondsLeft / 60
  );

  const seconds = secondsLeft % 60;

  return (
    <main className="exam-page">
      <header className="exam-header">
        <div>
          <span>COREPREP AI ASSESSMENT</span>

          <strong>{topic.title}</strong>
        </div>

        <div
          className={
            secondsLeft < 60
              ? "exam-timer danger"
              : "exam-timer"
          }
        >
          <Clock3 size={18} />

          {String(minutes).padStart(
            2,
            "0"
          )}
          :
          {String(seconds).padStart(
            2,
            "0"
          )}
        </div>
      </header>

      <div className="container exam-container">
        {submitError && (
          <div className="exam-info-banner">
            <AlertTriangle size={17} />
            <p>
              Submission was not completed. Your answers are saved on this device.
              {" "}{submitError} Please submit again.
            </p>
          </div>
        )}

        <div className="exam-info-banner">
          <AlertTriangle size={17} />

          <p>
            Submit before the timer reaches zero.
            The exam will automatically submit when
            time expires.
          </p>
        </div>

        <div className="exam-question-list">
          {questions.map(
            (question, index) => (
              <section
                key={question.id}
                className="exam-question-card"
              >
                <div className="exam-question-number">
                  Question {index + 1}

                  <span>
                    {question.type === "mcq"
                      ? "MCQ"
                      : "SHORT ANSWER"}
                  </span>
                </div>

                <h2>{question.question}</h2>

                {question.type === "mcq" ? (
                  <div className="exam-options">
                    {(question.options ?? []).map(
                      (option) => (
                        <label
                          key={option}
                          className={
                            answers[
                              question.id
                            ] === option
                              ? "exam-option selected"
                              : "exam-option"
                          }
                        >
                          <input
                            type="radio"
                            name={
                              String(question.id)
                            }
                            value={option}
                            checked={
                              answers[
                                question.id
                              ] === option
                            }
                            onChange={() =>
                              setAnswers(
                                (
                                  previous
                                ) => ({
                                  ...previous,
                                  [question.id]:
                                    option,
                                })
                              )
                            }
                          />

                          <span>{option}</span>
                        </label>
                      )
                    )}
                  </div>
                ) : (
                  <textarea
                    className="exam-short-answer"
                    placeholder="Write your answer here..."
                    value={
                      answers[
                        question.id
                      ] ?? ""
                    }
                    onChange={(event) =>
                      setAnswers(
                        (previous) => ({
                          ...previous,
                          [question.id]:
                            event.target
                              .value,
                        })
                      )
                    }
                  />
                )}
              </section>
            )
          )}
        </div>

        <div className="exam-submit-area">
          <div>
            <span>
              {
                Object.keys(answers)
                  .length
              }
              /{questions.length} answered
            </span>

            <p>
              You can submit even if some
              questions are unanswered.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={submitExam}
          >
            <Send size={17} />
            Submit Exam
          </button>
        </div>
      </div>
    </main>
  );
};

export default AssessmentExamPage;
