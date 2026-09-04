import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  AlertTriangle,
  ArrowLeft,
  BarChart3,
  Check,
  LogOut,
  Map,
  Save,
  Trash2,
  TrendingUp,
  UserRound,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { authService } from "../services/authService";
import { roadmapService } from "../services/roadmapService";
import { profileService } from "../services/profileService";
import type { PerformanceSummary, SubjectStatus } from "../types/profile";

const statusLabel: Record<SubjectStatus, string> = {
  weak: "Weak subject",
  needs_attention: "Needs attention",
  strong: "Strong",
  not_enough_data: "More data needed",
};

const ProfilePage = () => {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();
  const [roadmaps, setRoadmaps] = useState(roadmapService.getRoadmaps());
  const [name, setName] = useState(user?.name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [deletingRoadmapId, setDeletingRoadmapId] = useState<string | number | null>(null);
  const [roadmapError, setRoadmapError] = useState("");
  const [performance, setPerformance] = useState<PerformanceSummary | null>(null);
  const [performanceError, setPerformanceError] = useState("");
  const [performanceLoading, setPerformanceLoading] = useState(true);

  useEffect(() => {
    roadmapService.fetchRoadmaps().then(setRoadmaps).catch(() => {
      // Keep the last cached list when the API is temporarily unavailable.
    });
  }, []);

  useEffect(() => {
    profileService.getPerformance()
      .then(setPerformance)
      .catch((cause) => setPerformanceError(
        cause instanceof Error ? cause.message : "Performance data could not be loaded.",
      ))
      .finally(() => setPerformanceLoading(false));
  }, []);

  if (!user) {
    return (
      <>
        <Navbar />
        <main className="profile-page profile-empty-page">
          <UserRound size={30} />
          <h1>Sign in to view your profile</h1>
          <Link to="/signin" className="primary-button">Sign In</Link>
        </main>
      </>
    );
  }

  const saveDetails = (event: FormEvent) => {
    event.preventDefault();
    if (password && password !== confirmPassword) {
      setError("Passwords do not match.");
      setMessage("");
      return;
    }

    localStorage.setItem("coreprep_user", JSON.stringify({ ...user, name: name.trim(), email: email.trim() }));
    if (password) {
      authService.updatePassword(password);
    }
    window.dispatchEvent(new Event("coreprep-auth-change"));
    setPassword("");
    setConfirmPassword("");
    setError("");
    setMessage("Personal details updated.");
  };

  const signOut = () => {
    authService.signOut();
    navigate("/");
  };

  const deleteRoadmap = async (roadmapId: string | number, title: string) => {
    if (!window.confirm(`Delete "${title}"? This will also delete its assessments and progress.`)) {
      return;
    }
    setDeletingRoadmapId(roadmapId);
    setRoadmapError("");
    try {
      await roadmapService.deleteRoadmap(roadmapId);
      setRoadmaps((items) => items.filter((item) => item.id !== roadmapId));
    } catch (cause) {
      setRoadmapError(cause instanceof Error ? cause.message : "Could not delete the roadmap.");
    } finally {
      setDeletingRoadmapId(null);
    }
  };

  return (
    <>
      <Navbar />
      <main className="profile-page">
        <div className="container profile-container">
          <Link to="/" className="company-back-link"><ArrowLeft size={17} />Back to Home</Link>
          <div className="profile-page-heading">
            <span className="hero-badge"><UserRound size={15} />My Profile</span>
            <h1>Personal information</h1>
            <p>Manage your account details and access your preparation roadmap.</p>
          </div>

          <div className="profile-layout">
            <section className="profile-panel">
              <div className="profile-panel-heading">
                <div className="profile-avatar">{name.slice(0, 1).toUpperCase()}</div>
                <div><span>ACCOUNT DETAILS</span><h2>{name || "Your profile"}</h2></div>
              </div>
              <form onSubmit={saveDetails}>
                <div className="profile-input-group"><label htmlFor="profile-name">Full name</label><input id="profile-name" value={name} onChange={(event) => setName(event.target.value)} required /></div>
                <div className="profile-input-group"><label htmlFor="profile-email">Email address</label><input id="profile-email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></div>
                <div className="profile-input-group"><label htmlFor="profile-password">New password</label><input id="profile-password" type="password" placeholder="Leave blank to keep current password" value={password} onChange={(event) => setPassword(event.target.value)} /></div>
                <div className="profile-input-group"><label htmlFor="profile-confirm-password">Confirm new password</label><input id="profile-confirm-password" type="password" placeholder="Re-enter new password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} /></div>
                {error && <p className="profile-error">{error}</p>}
                {message && <p className="profile-success"><Check size={15} />{message}</p>}
                <button className="primary-button" type="submit"><Save size={16} />Save Changes</button>
              </form>
            </section>

            <section className="profile-panel profile-roadmap-panel">
              <div className="profile-panel-heading"><div className="profile-panel-icon"><Map size={20} /></div><div><span>YOUR ROADMAPS</span><h2>Created roadmaps</h2></div></div>
              {roadmaps.length ? (
                <div className="profile-roadmap-list">
                  {roadmaps.map((item) => (
                    <div className="profile-roadmap-row" key={item.id}>
                      <Link
                        to="/roadmap/current"
                        className="profile-roadmap-item"
                        onClick={() => roadmapService.selectRoadmap(item)}
                      >
                      <div><strong>{item.title}</strong><span>{item.weeks} weeks · {item.topics.length} topics</span></div><ArrowLeft size={17} />
                      </Link>
                      <button
                        type="button"
                        className="profile-roadmap-delete"
                        aria-label={`Delete ${item.title}`}
                        title="Delete roadmap"
                        disabled={deletingRoadmapId === item.id}
                        onClick={() => deleteRoadmap(item.id, item.title)}
                      >
                        <Trash2 size={17} />
                      </button>
                    </div>
                  ))}
                  {roadmapError && <p className="profile-error">{roadmapError}</p>}
                </div>
              ) : (
                <p className="profile-muted">No roadmap created yet. Your roadmap will appear here after you create one.</p>
              )}
            </section>
          </div>

          <section className="profile-panel profile-performance-panel">
            <div className="profile-panel-heading profile-performance-heading">
              <div className="profile-panel-icon"><BarChart3 size={20} /></div>
              <div>
                <span>EXAM INSIGHTS</span>
                <h2>Subject performance</h2>
                <p>Your weakness score is calculated from incorrect answers across submitted roadmap exams.</p>
              </div>
              {performance && performance.total_answered > 0 && (
                <div className="profile-accuracy-summary">
                  <strong>{performance.overall_accuracy}%</strong>
                  <span>overall accuracy</span>
                </div>
              )}
            </div>

            {performanceLoading ? (
              <div className="profile-performance-state"><span className="cv-loader" />Loading exam insights...</div>
            ) : performanceError ? (
              <p className="profile-error">{performanceError}</p>
            ) : !performance?.subjects.length ? (
              <div className="profile-performance-empty">
                <TrendingUp size={24} />
                <div>
                  <h3>No exam results yet</h3>
                  <p>Complete roadmap assessments to discover your strong and weak subjects.</p>
                </div>
              </div>
            ) : (
              <>
                {performance.weak_subjects.length > 0 && (
                  <div className="profile-weak-alert">
                    <AlertTriangle size={18} />
                    <div>
                      <strong>Focus recommended</strong>
                      <span>{performance.weak_subjects.join(", ")} {performance.weak_subjects.length === 1 ? "is" : "are"} currently marked weak.</span>
                    </div>
                  </div>
                )}
                <div className="profile-performance-chart">
                  {performance.subjects.map((item) => (
                    <article className="profile-subject-row" key={item.subject}>
                      <div className="profile-subject-label">
                        <div><strong>{item.subject}</strong><span>{item.incorrect} incorrect of {item.answered} answered</span></div>
                        <span className={`profile-status profile-status-${item.status}`}>{statusLabel[item.status]}</span>
                      </div>
                      <div className="profile-weakness-track" aria-label={`${item.subject} weakness score ${item.weakness_score}%`}>
                        <div className={`profile-weakness-fill profile-fill-${item.status}`} style={{ width: `${item.weakness_score}%` }} />
                      </div>
                      <div className="profile-subject-scale"><span>0% weakness</span><strong>{item.weakness_score}%</strong><span>100% weakness</span></div>
                    </article>
                  ))}
                </div>
                <p className="profile-performance-note">
                  A subject needs at least 3 answered questions before classification. Weak means 50% or more incorrect; needs attention means 30–49% incorrect.
                </p>
              </>
            )}
          </section>

          <button type="button" className="profile-signout" onClick={signOut}><LogOut size={16} />Sign Out</button>
        </div>
      </main>
      <Footer />
    </>
  );
};

export default ProfilePage;
