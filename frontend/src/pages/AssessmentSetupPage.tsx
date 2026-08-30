import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import {
  ArrowLeft,
  Clock3,
  FileQuestion,
  ListChecks,
  Play,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

import { roadmapService } from "../services/roadmapService";

const AssessmentSetupPage = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const roadmap =
    roadmapService.getRoadmap();

  const topic = roadmap?.topics.find(
    (item) => String(item.id) === topicId
  );

  const [mcqCount, setMcqCount] =
    useState(10);

  const [shortCount, setShortCount] =
    useState(3);

  const [duration, setDuration] =
    useState(20);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  if (!roadmap || !topic || !topicId) {
    return (
      <>
        <Navbar />

        <main className="assessment-missing">
          <h1>Assessment not found</h1>

          <Link
            to="/roadmap/current"
            className="primary-button"
          >
            Return to Roadmap
          </Link>
        </main>
      </>
    );
  }

  const startExam = async () => {
    if (mcqCount + shortCount < 1) {
      setError("Select at least one MCQ or short-answer question.");
      return;
    }
    setGenerating(true);
    setError("");
    roadmapService.saveAssessmentConfig({
      topicId,
      mcqCount,
      shortCount,
      durationMinutes: duration,
    });

    try {
      await roadmapService.generateAssessment(
        roadmap.id,
        topic.id,
        mcqCount,
        shortCount,
        duration,
      );
      navigate(`/roadmap/assessment/${topicId}/exam`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not generate the assessment.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <>
      <Navbar />

      <main className="assessment-setup-page">
        <div className="container assessment-container">
          <Link
            to="/roadmap/current"
            className="company-back-link"
          >
            <ArrowLeft size={17} />
            Back to Roadmap
          </Link>

          <div className="assessment-setup-heading">
            <span>TOPIC ASSESSMENT</span>

            <h1>{topic.title}</h1>

            <p>
              Customize the assessment before
              starting your exam.
            </p>
          </div>

          <div className="assessment-config-grid">
            <div className="assessment-config-card">
              <div className="assessment-config-icon">
                <ListChecks size={22} />
              </div>

              <h3>MCQ Questions</h3>

              <p>
                Choose the number of multiple-choice
                questions.
              </p>

              <input
                type="number"
                min="0"
                max="10"
                value={mcqCount}
                onChange={(event) =>
                  setMcqCount(
                    Math.max(
                      0,
                      Math.min(
                        10,
                        Number(
                          event.target.value
                        )
                      )
                    )
                  )
                }
              />
            </div>

            <div className="assessment-config-card">
              <div className="assessment-config-icon">
                <FileQuestion size={22} />
              </div>

              <h3>Short Questions</h3>

              <p>
                Add conceptual short-answer
                questions.
              </p>

              <input
                type="number"
                min="0"
                max="10"
                value={shortCount}
                onChange={(event) =>
                  setShortCount(
                    Math.max(
                      0,
                      Math.min(
                        10,
                        Number(
                          event.target.value
                        )
                      )
                    )
                  )
                }
              />
            </div>

            <div className="assessment-config-card">
              <div className="assessment-config-icon">
                <Clock3 size={22} />
              </div>

              <h3>Duration</h3>

              <p>
                Set the total exam duration in
                minutes.
              </p>

              <input
                type="number"
                min="5"
                max="120"
                value={duration}
                onChange={(event) =>
                  setDuration(
                    Math.max(
                      5,
                      Math.min(
                        120,
                        Number(
                          event.target.value
                        )
                      )
                    )
                  )
                }
              />
            </div>
          </div>

          <div className="assessment-summary-card">
            <div>
              <span>ASSESSMENT SUMMARY</span>

              <h2>
                {mcqCount + shortCount} Questions
              </h2>

              <p>
                {mcqCount} MCQ • {shortCount} Short
                Answer • {duration} Minutes
              </p>
            </div>

            {error && <p className="roadmap-error">{error}</p>}
            <button
              className="primary-button"
              onClick={startExam}
              disabled={generating}
            >
              <Play size={17} />
              {generating ? "Generating Questions..." : "Start Exam"}
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default AssessmentSetupPage;
