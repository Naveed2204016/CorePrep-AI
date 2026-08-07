import { useState } from "react";
import { Link } from "react-router-dom";
import {
  BrainCircuit,
  Menu,
  X,
} from "lucide-react";

const Navbar = () => {
  const [open, setOpen] = useState(false);

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <Link to="/" className="logo">
          <span className="logo-icon">
            <BrainCircuit size={21} />
          </span>

          <span>
            CorePrep <strong>AI</strong>
          </span>
        </Link>

        <nav className="desktop-nav">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#subjects">Subjects</a>
        </nav>

        <div className="desktop-auth">
          <Link to="/signin" className="signin-link">
            Sign In
          </Link>

          <Link to="/signup" className="primary-button">
            Get Started
          </Link>
        </div>

        <button
          className="mobile-menu-button"
          onClick={() => setOpen(!open)}
          aria-label="Open navigation menu"
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="mobile-nav">
          <a href="#features" onClick={() => setOpen(false)}>
            Features
          </a>

          <a
            href="#how-it-works"
            onClick={() => setOpen(false)}
          >
            How It Works
          </a>

          <a href="#subjects" onClick={() => setOpen(false)}>
            Subjects
          </a>

          <Link to="/signin" onClick={() => setOpen(false)}>
            Sign In
          </Link>

          <Link
            to="/signup"
            className="primary-button"
            onClick={() => setOpen(false)}
          >
            Get Started
          </Link>
        </div>
      )}
    </header>
  );
};

export default Navbar;