import { useState } from "react";
import type { ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import {
  ArrowLeft,
  BriefcaseBusiness,
  CalendarDays,
  Check,
  FileText,
  Map,
  Sparkles,
  UploadCloud,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

import {
  roadmapService,
  SUPPORTED_TOPICS,
} from "../services/roadmapService";

import type { RoadmapMode } from "../types/roadmap";

const RoadmapCreatePage = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState<RoadmapMode>("topic");
  const [topic, setTopic] = useState("Data Structures & Algorithms");
  const [jobFile, setJobFile] = useState<File | null>(null);
  const [weeks, setWeeks] = useState(4);
  const [error, setError] = useState("");
  const [generating, setGenerating] = useState(false);

  const timelineOptions = mode === "topic" ? [4, 6, 8, 10, 12] : [6, 8, 10, 12];

  const selectMode = (newMode: RoadmapMode) => {
    setMode(newMode);
    setError("");
    setWeeks(newMode === "topic" ? 4 : 6);
  };

  const handleJobFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (file.type !== "application/pdf") {
      setError("Please upload the job description in PDF format.");
      return;
    }
    setError("");
    setJobFile(file);
  };

  const generateRoadmap = async () => {
    if (mode === "job" && !jobFile) {
      setError("Please upload a job description first.");
      return;
    }
    setGenerating(true);
    setError("");
    await roadmapService.generateRoadmap({
      mode,
      weeks,
      topic: mode === "topic" ? topic : undefined,
      jobFileName: mode === "job" ? jobFile?.name : undefined,
    });
    setGenerating(false);
    navigate("/roadmap/current");
  };

  return (
    <>
      <Navbar />
      <main className="roadmap-page">
        <div className="roadmap-glow" />
        <div className="container roadmap-container">
          <Link to="/" className="company-back-link"><ArrowLeft size={17} />Back to Home</Link>
          <motion.div className="roadmap-page-heading" initial={{ opacity: 0, y: 25 }} animate={{ opacity: 1, y: 0 }}>
            <div className="hero-badge"><Sparkles size={15} />Personalized Preparation</div>
            <h1>Build your interview<br />preparation <span>roadmap.</span></h1>
            <p>Choose a CS topic or upload a target job description. CorePrep AI will organize your preparation into a structured timeline.</p>
          </motion.div>
          <div className="roadmap-mode-grid">
            <button className={`roadmap-mode-card ${mode === "topic" ? "selected" : ""}`} onClick={() => selectMode("topic")}>
              <div className="roadmap-mode-icon"><Map size={24} /></div>
              <div><span>TOPIC BASED</span><h3>Choose a Topic</h3><p>Prepare systematically for a specific computer science subject.</p></div>
              {mode === "topic" && <Check className="roadmap-selected-check" />}
            </button>
            <button className={`roadmap-mode-card ${mode === "job" ? "selected" : ""}`} onClick={() => selectMode("job")}>
              <div className="roadmap-mode-icon"><BriefcaseBusiness size={24} /></div>
              <div><span>JOB FOCUSED</span><h3>Upload Job Description</h3><p>Build preparation around a target software engineering role.</p></div>
              {mode === "job" && <Check className="roadmap-selected-check" />}
            </button>
          </div>
          <section className="roadmap-builder-card">
            {mode === "topic" ? (
              <>
                <div className="roadmap-builder-heading"><Map size={21} /><div><h2>Select Your Topic</h2><p>Choose the subject you want to prepare.</p></div></div>
                <div className="roadmap-topic-grid">{SUPPORTED_TOPICS.map((item) => <button key={item} className={topic === item ? "roadmap-topic-option selected" : "roadmap-topic-option"} onClick={() => setTopic(item)}>{item}{topic === item && <Check size={14} />}</button>)}</div>
              </>
            ) : (
              <>
                <div className="roadmap-builder-heading"><FileText size={21} /><div><h2>Upload Job Description</h2><p>Upload the target role in PDF format.</p></div></div>
                <label className="roadmap-job-upload"><input type="file" accept=".pdf,application/pdf" hidden onChange={handleJobFile} /><UploadCloud size={29} />{jobFile ? <><strong>{jobFile.name}</strong><span>Click to choose another file</span></> : <><strong>Choose job description PDF</strong><span>The AI skill extraction will be connected later.</span></>}</label>
              </>
            )}
            <div className="roadmap-timeline-section">
              <div className="roadmap-builder-heading"><CalendarDays size={21} /><div><h2>Choose Timeline</h2><p>Minimum {mode === "topic" ? "4" : "6"} weeks for this roadmap.</p></div></div>
              <div className="roadmap-week-options">{timelineOptions.map((option) => <button key={option} className={weeks === option ? "roadmap-week selected" : "roadmap-week"} onClick={() => setWeeks(option)}><strong>{option}</strong><span>weeks</span></button>)}</div>
            </div>
            {error && <p className="roadmap-error">{error}</p>}
            <button className="primary-button roadmap-generate-button" onClick={generateRoadmap} disabled={generating}><Sparkles size={17} />{generating ? "Generating Roadmap..." : "Generate Roadmap"}</button>
          </section>
        </div>
      </main>
      <Footer />
    </>
  );
};

export default RoadmapCreatePage;
