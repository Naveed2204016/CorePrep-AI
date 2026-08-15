import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import CompanyPrepPage from "./pages/CompanyPrepPage";
import CompanyExamSetupPage from "./pages/CompanyExamSetupPage";
import CVReviewPage from "./pages/CVReviewPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/signin"
          element={<SignInPage />}
        />
        <Route
          path="/signup"
          element={<SignUpPage />}
        />
        <Route
          path="/company-prep"
          element={<CompanyPrepPage />}
        />
        <Route
          path="/company-prep/:companySlug"
          element={<CompanyExamSetupPage />}
        />
        <Route
          path="/cv-review"
          element={<CVReviewPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;