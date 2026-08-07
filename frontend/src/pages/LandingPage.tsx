import { motion } from "framer-motion";
import { Link } from "react-router-dom";

import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  FileSearch,
  Map,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import FeatureCard from "../components/ui/FeatureCard";

import heroImage from "../assets/hero.png";

const subjects = [
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

const LandingPage = () => {
  return (
    <div>
      <Navbar />

      <main>
        {/* HERO */}

        <section className="hero-section">
          <div className="hero-glow hero-glow-1" />
          <div className="hero-glow hero-glow-2" />

          <div className="container hero-grid">
            <motion.div
              initial={{ opacity: 0, x: -45 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.65 }}
            >
              <div className="hero-badge">
                <Sparkles size={15} />
                AI-Powered Interview Preparation
              </div>

              <h1 className="hero-title">
                Prepare Smarter.
                <br />
                Interview <span>Better.</span>
              </h1>

              <p className="hero-text">
                Build personalized preparation roadmaps,
                practice company-focused interview questions,
                improve your CV and track your progress from one
                intelligent platform.
              </p>

              <div className="hero-buttons">
                <Link to="/signup" className="primary-button hero-btn">
                  Start Preparing
                  <ArrowRight size={18} />
                </Link>

                <a
                  href="#features"
                  className="secondary-button hero-btn"
                >
                  Explore Features
                </a>
              </div>

              <div className="hero-benefits">
                <span>
                  <CheckCircle2 size={16} />
                  Personalized
                </span>

                <span>
                  <CheckCircle2 size={16} />
                  RAG Powered
                </span>

                <span>
                  <CheckCircle2 size={16} />
                  Progress Focused
                </span>
              </div>
            </motion.div>

            <motion.div
              className="hero-image-wrapper"
              initial={{ opacity: 0, x: 45 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                duration: 0.65,
                delay: 0.15,
              }}
            >
              <img
                src={heroImage}
                alt="CorePrep AI interview preparation"
                className="hero-image"
              />

              <motion.div
                className="floating-box floating-box-1"
                animate={{ y: [0, -8, 0] }}
                transition={{
                  repeat: Infinity,
                  duration: 3.5,
                }}
              >
                <Sparkles size={17} />
                AI Roadmap Ready
              </motion.div>

              <motion.div
                className="floating-box floating-box-2"
                animate={{ y: [0, 8, 0] }}
                transition={{
                  repeat: Infinity,
                  duration: 4,
                }}
              >
                Interview Readiness: 82%
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* FEATURES */}

        <section className="section" id="features">
          <div className="container">
            <motion.div
              className="section-heading"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{
                opacity: 1,
                y: 0,
              }}
              viewport={{ once: true }}
            >
              <span>CORE FEATURES</span>

              <h2>Your interview preparation command center.</h2>

              <p>
                Organize your preparation, practice intelligently
                and focus on what matters most.
              </p>
            </motion.div>

            <div className="features-grid">
              <motion.div
                initial={{ opacity: 0, y: 35 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
              >
                <FeatureCard
                  icon={Map}
                  title="Create Roadmap"
                  description="Create a personalized preparation roadmap based on your subjects, skill level, available time and target role."
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 35 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.12 }}
              >
               <FeatureCard
                icon={BriefcaseBusiness}
                title="Company Specific Exam"
                description="Practice company-specific and subject-focused interview questions through structured mock examinations."
                to="/company-prep"
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 35 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.24 }}
              >
                <FeatureCard
                  icon={FileSearch}
                  title="Review CV"
                  description="Upload your CV and receive AI-assisted feedback before applying for software engineering positions."
                />
              </motion.div>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS */}

        <section
          className="section alternate-section"
          id="how-it-works"
        >
          <div className="container">
            <div className="section-heading">
              <span>HOW IT WORKS</span>
              <h2>A clear path from preparation to progress.</h2>
            </div>

            <div className="steps-grid">
              <div className="step-card">
                <span>01</span>
                <h3>Choose Your Goal</h3>
                <p>
                  Select subjects or provide a target job
                  description.
                </p>
              </div>

              <div className="step-card">
                <span>02</span>
                <h3>Get Your Roadmap</h3>
                <p>
                  AI organizes your topics and preparation
                  priorities.
                </p>
              </div>

              <div className="step-card">
                <span>03</span>
                <h3>Practice & Improve</h3>
                <p>
                  Take assessments and improve based on your
                  performance.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* SUBJECTS */}

        <section className="section" id="subjects">
          <div className="container">
            <div className="section-heading">
              <span>CS & SOFTWARE ENGINEERING</span>

              <h2>Prepare across the topics that matter.</h2>
            </div>

            <div className="subjects-grid">
              {subjects.map((subject) => (
                <div key={subject} className="subject-pill">
                  {subject}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FINAL CTA */}

        <section className="section">
          <div className="container">
            <div className="cta-box">
              <div>
                <span>READY TO START?</span>

                <h2>
                  Turn scattered preparation into a clear plan.
                </h2>
              </div>

              <Link to="/signup" className="primary-button">
                Get Started
                <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default LandingPage;