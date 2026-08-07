import { BrainCircuit } from "lucide-react";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container footer-grid">
        <div>
          <div className="footer-logo">
            <BrainCircuit size={22} />
            CorePrep AI
          </div>

          <p>
            AI-powered preparation for computer science and
            software engineering interviews.
          </p>
        </div>

        <div>
          <h4>Platform</h4>
          <a href="#features">Create Roadmap</a>
          <a href="#features">Company Prep</a>
          <a href="#features">CV Review</a>
        </div>

        <div>
          <h4>Explore</h4>
          <a href="#subjects">Subjects</a>
          <a href="#how-it-works">How It Works</a>
        </div>
      </div>

      <div className="container footer-bottom">
        © 2026 CorePrep AI
      </div>
    </footer>
  );
};

export default Footer;