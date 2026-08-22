import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowLeft, Check, LogOut, Map, Save, UserRound } from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { authService } from "../services/authService";
import { roadmapService } from "../services/roadmapService";

const ProfilePage = () => {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();
  const roadmaps = roadmapService.getRoadmaps();
  const [name, setName] = useState(user?.name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

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
                    <Link
                      to="/roadmap/current"
                      className="profile-roadmap-item"
                      key={item.id}
                      onClick={() => roadmapService.selectRoadmap(item)}
                    >
                      <div><strong>{item.title}</strong><span>{item.weeks} weeks · {item.topics.length} topics</span></div><ArrowLeft size={17} />
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="profile-muted">No roadmap created yet. Your roadmap will appear here after you create one.</p>
              )}
            </section>
          </div>

          <button type="button" className="profile-signout" onClick={signOut}><LogOut size={16} />Sign Out</button>
        </div>
      </main>
      <Footer />
    </>
  );
};

export default ProfilePage;
