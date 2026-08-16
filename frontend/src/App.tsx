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
import RoadmapCreatePage from "./pages/RoadmapCreatePage";
import RoadmapPreviewPage from "./pages/RoadmapPreviewPage";
import AssessmentSetupPage from "./pages/AssessmentSetupPage";
import AssessmentExamPage from "./pages/AssessmentExamPage";
import AssessmentResultPage from "./pages/AssessmentResultPage";

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
        <Route
        path="/roadmap/create"
        element={<RoadmapCreatePage />}
        />

        <Route
        path="/roadmap/current"
        element={<RoadmapPreviewPage />}
        />

       <Route
       path="/roadmap/assessment/:topicId/setup"
       element={<AssessmentSetupPage />}
       />

      <Route
      path="/roadmap/assessment/:topicId/exam"
      element={<AssessmentExamPage />}
      />

      <Route
      path="/roadmap/assessment/:topicId/result"
      element={<AssessmentResultPage />}
      />
      </Routes>
    </BrowserRouter>
  );
}

export default App;