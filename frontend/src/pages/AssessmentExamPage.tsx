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
    (item) => item.id === topicId
  );

  const questions =
    topic && config
      ? roadmapService.generateQuestions(
          topic.title,
          config.mcqCount,
          config.shortCount
        )
      : [];

  const [answers, setAnswers] = useState<
    Record<string, string>
  >({});

  const [secondsLeft, setSecondsLeft] =
    useState(
      config
        ? config.durationMinutes * 60
        : 0
    );

  const submitted = useRef(false);

  const submitExam = useCallback(() => {
    if (
      submitted.current ||
      !topicId ||
      questions.length === 0
    ) {
      return;
    }

    submitted.current = true;

    const result =
      roadmapService.evaluateExam(
        topicId,
        questions,
        answers
      );

    sessionStorage.setItem(
      "coreprep_exam_result",
      JSON.stringify(result)
    );

    if (result.passed) {
      roadmapService.markTopicCompleted(
        topicId
      );
    }

    navigate(
      `/roadmap/assessment/${topicId}/result`
    );
  }, [
    answers,
    navigate,
    questions,
    topicId,
  ]);

  useEffect(() => {
    if (!config) return;

    const interval = setInterval(() => {
      setSecondsLeft((previous) =>
        previous > 0 ? previous - 1 : 0
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [config]);

  useEffect(() => {
    if (
      secondsLeft === 0 &&
      config &&
      !submitted.current
    ) {
      submitExam();
    }
  }, [
    secondsLeft,
    config,
    submitExam,
  ]);

  if (
    !roadmap ||
    !config ||
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
                    {question.options.map(
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
                              question.id
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