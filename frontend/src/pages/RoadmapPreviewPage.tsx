import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

import {
  ArrowLeft,
  BookOpen,
  Check,
  CheckCircle2,
  Clock3,
  ExternalLink,
  Lock,
  PencilLine,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

import { roadmapService } from "../services/roadmapService";

const RoadmapPreviewPage = () => {
  const initialRoadmap =
    roadmapService.getRoadmap();

  const [roadmap, setRoadmap] =
    useState(initialRoadmap);

  const [showEdit, setShowEdit] =
    useState(false);

  const [suggestion, setSuggestion] =
    useState("");

  const [editMessage, setEditMessage] =
    useState("");

  const completedTopics =
    roadmapService.getCompletedTopics();

  if (!roadmap) {
    return (
      <>
        <Navbar />

        <main className="roadmap-empty-page">
          <Sparkles size={34} />

          <h1>No roadmap generated yet</h1>

          <p>
            Create your first personalized preparation
            roadmap.
          </p>

          <Link
            to="/roadmap/create"
            className="primary-button"
          >
            Create Roadmap
          </Link>
        </main>
      </>
    );
  }

  const confirmRoadmap = () => {
    const updated = {
      ...roadmap,
      confirmed: true,
    };

    roadmapService.saveRoadmap(updated);
    setRoadmap(updated);

    setShowEdit(false);
    setEditMessage("");
  };

  const submitSuggestion = () => {
    if (!suggestion.trim()) return;

    const updated = {
      ...roadmap,
      confirmed: false,
      editNote: suggestion,
    };

    roadmapService.saveRoadmap(updated);
    setRoadmap(updated);

    setEditMessage(
      "Suggestion saved. In the final version the AI will regenerate the roadmap based on this feedback."
    );

    setSuggestion("");
  };

  const completedCount =
    roadmap.topics.filter((topic) =>
      completedTopics.includes(topic.id)
    ).length;

  const progress = Math.round(
    (completedCount / roadmap.topics.length) *
      100
  );

  return (
    <>
      <Navbar />

      <main className="roadmap-page">
        <div className="roadmap-glow" />

        <div className="container roadmap-container">
          <Link
            to="/roadmap/create"
            className="company-back-link"
          >
            <ArrowLeft size={17} />
            Create Another Roadmap
          </Link>

          <div className="roadmap-preview-top">
            <div>
              <div className="hero-badge">
                <Sparkles size={15} />
                AI-Generated Roadmap
              </div>

              <h1>{roadmap.title}</h1>

              <p>
                {roadmap.weeks} weeks • Based on{" "}
                {roadmap.sourceLabel}
              </p>
            </div>

            <div className="roadmap-status-box">
              <span>PROGRESS</span>

              <strong>{progress}%</strong>

              <small>
                {completedCount}/
                {roadmap.topics.length} topics
              </small>
            </div>
          </div>

          <div className="roadmap-progress-bar">
            <div
              style={{
                width: `${progress}%`,
              }}
            />
          </div>

          {!roadmap.confirmed && (
            <section className="roadmap-decision-card">
              <div>
                <span>ROADMAP REVIEW</span>

                <h2>
                  Does this preparation plan look right?
                </h2>

                <p>
                  Confirm it to unlock topic assessments,
                  or suggest an edit before continuing.
                </p>
              </div>

              <div className="roadmap-decision-actions">
                <button
                  className="secondary-button"
                  onClick={() =>
                    setShowEdit(!showEdit)
                  }
                >
                  <PencilLine size={16} />
                  Suggest Edit
                </button>

                <button
                  className="primary-button"
                  onClick={confirmRoadmap}
                >
                  <Check size={17} />
                  Confirm Roadmap
                </button>
              </div>

              {showEdit && (
                <div className="roadmap-edit-box">
                  <textarea
                    placeholder="Example: Give more time to System Design and reduce basic frontend topics..."
                    value={suggestion}
                    onChange={(event) =>
                      setSuggestion(
                        event.target.value
                      )
                    }
                  />

                  <button
                    className="primary-button"
                    onClick={submitSuggestion}
                  >
                    Submit Suggestion
                  </button>
                </div>
              )}

              {editMessage && (
                <p className="roadmap-edit-message">
                  {editMessage}
                </p>
              )}
            </section>
          )}

          {roadmap.confirmed && (
            <div className="roadmap-confirmed-banner">
              <CheckCircle2 size={19} />

              <div>
                <strong>
                  Roadmap Confirmed
                </strong>

                <span>
                  Assessments are now available.
                </span>
              </div>
            </div>
          )}

          <div className="roadmap-topic-list">
            {roadmap.topics.map(
              (topic, index) => {
                const completed =
                  completedTopics.includes(
                    topic.id
                  );

                return (
                  <motion.article
                    className={
                      completed
                        ? "generated-topic-card completed"
                        : "generated-topic-card"
                    }
                    key={topic.id}
                    initial={{
                      opacity: 0,
                      y: 25,
                    }}
                    animate={{
                      opacity: 1,
                      y: 0,
                    }}
                    transition={{
                      delay: index * 0.07,
                    }}
                  >
                    <div className="topic-timeline-column">
                      <div className="topic-number">
                        {completed ? (
                          <Check size={17} />
                        ) : (
                          index + 1
                        )}
                      </div>

                      {index <
                        roadmap.topics.length -
                          1 && (
                        <div className="topic-line" />
                      )}
                    </div>

                    <div className="generated-topic-content">
                      <div className="generated-topic-heading">
                        <div>
                          <span>
                            <Clock3 size={14} />
                            {topic.dayRange}
                          </span>

                          <h2>{topic.title}</h2>
                        </div>

                        {completed && (
                          <div className="topic-completed-badge">
                            <CheckCircle2
                              size={14}
                            />
                            Completed
                          </div>
                        )}
                      </div>

                      <p>{topic.description}</p>

                      <div className="topic-resource-list">
                        <span className="resource-title">
                          <BookOpen size={15} />
                          Recommended Resources
                        </span>

                        {topic.resources.map(
                          (resource) => (
                            <a
                              key={resource.title}
                              href={resource.url}
                              target="_blank"
                              rel="noreferrer"
                            >
                              <div>
                                <strong>
                                  {resource.title}
                                </strong>

                                <span>
                                  {resource.type}
                                </span>
                              </div>

                              <ExternalLink
                                size={15}
                              />
                            </a>
                          )
                        )}
                      </div>

                      {!completed &&
                        (roadmap.confirmed ? (
                          <Link
                            to={`/roadmap/assessment/${topic.id}/setup`}
                            className="primary-button topic-assessment-button"
                          >
                            Take Assessment
                          </Link>
                        ) : (
                          <div className="assessment-locked">
                            <Lock size={14} />
                            Confirm roadmap to unlock
                            assessment
                          </div>
                        ))}
                    </div>
                  </motion.article>
                );
              }
            )}
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default RoadmapPreviewPage;