import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

import {
  ArrowLeft,
  ArrowRight,
  Building2,
  Search,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { companies } from "../features/company-prep/data/companies";

const CompanyPrepPage = () => {
  const [search, setSearch] = useState("");

  const filteredCompanies = useMemo(() => {
    return companies.filter((company) =>
      company.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [search]);

  return (
    <>
      <Navbar />

      <main className="company-prep-page">
        <section className="company-prep-hero">
          <div className="company-page-glow company-glow-one" />
          <div className="company-page-glow company-glow-two" />

          <div className="container">
            <Link to="/" className="company-back-link">
              <ArrowLeft size={17} />
              Back to Home
            </Link>

            <motion.div
              className="company-page-heading"
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="hero-badge">
                <Sparkles size={15} />
                Company-Specific Preparation
              </div>

              <h1>
                Prepare for the companies
                <br />
                you want to <span>join.</span>
              </h1>

              <p>
                Choose a company and practice interview questions
                collected from previous interview experiences.
              </p>
            </motion.div>

            <motion.div
              className="company-search"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
            >
              <Search size={19} />

              <input
                type="text"
                placeholder="Search companies..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />

              <span>{filteredCompanies.length} companies</span>
            </motion.div>
          </div>
        </section>

        <section className="company-list-section">
          <div className="container">
            {filteredCompanies.length > 0 ? (
              <div className="company-grid">
                {filteredCompanies.map((company, index) => (
                  <motion.div
                    key={company.slug}
                    initial={{ opacity: 0, y: 25 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                      duration: 0.35,
                      delay: Math.min(index * 0.025, 0.35),
                    }}
                  >
                    <Link
                      to={`/company-prep/${company.slug}`}
                      className="company-card"
                    >
                      <div className="company-card-top">
                        <div className="company-avatar">
                          {company.shortName}
                        </div>

                        <ArrowRight
                          className="company-card-arrow"
                          size={19}
                        />
                      </div>

                      <div className="company-card-content">
                        <h3>{company.name}</h3>

                        <p>
                          Practice interview questions collected
                          from previous candidates.
                        </p>
                      </div>

                      <div className="company-card-footer">
                        <Building2 size={15} />
                        Start company preparation
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="company-empty-state">
                <Search size={30} />

                <h3>No companies found</h3>

                <p>
                  Try searching with a different company name.
                </p>
              </div>
            )}

            <p className="company-source-note">
              Company list based on the Interview BD community
              interview-question collection.
            </p>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
};

export default CompanyPrepPage;