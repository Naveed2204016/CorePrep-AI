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
import CompanyExamPage from "./pages/CompanyExamPage";
import CompanyExamResultPage from "./pages/CompanyExamResultPage";
import CVReviewPage from "./pages/CVReviewPage";
import RoadmapCreatePage from "./pages/RoadmapCreatePage";
import RoadmapPreviewPage from "./pages/RoadmapPreviewPage";
import AssessmentSetupPage from "./pages/AssessmentSetupPage";
import AssessmentExamPage from "./pages/AssessmentExamPage";
import AssessmentResultPage from "./pages/AssessmentResultPage";
import ProfilePage from "./pages/ProfilePage";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import OAuthSuccessPage from "./pages/OAuthSuccessPage";

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
          path="/oauth-success"
          element={<OAuthSuccessPage />}
        />
        <Route
          path="/company-prep"
          element={
            <ProtectedRoute>
              <CompanyPrepPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/company-prep/:companySlug/result"
          element={
            <ProtectedRoute>
              <CompanyExamResultPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/company-prep/:companySlug/exam"
          element={
            <ProtectedRoute>
              <CompanyExamPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/company-prep/:companySlug"
          element={
            <ProtectedRoute>
              <CompanyExamSetupPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/cv-review"
          element={
            <ProtectedRoute>
              <CVReviewPage />
            </ProtectedRoute>
          }
        />
        <Route
        path="/roadmap/create"
        element={
          <ProtectedRoute>
            <RoadmapCreatePage />
          </ProtectedRoute>
        }
        />

        <Route
        path="/roadmap/current"
        element={
          <ProtectedRoute>
            <RoadmapPreviewPage />
          </ProtectedRoute>
        }
        />

        <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        }
        />

       <Route
       path="/roadmap/assessment/:topicId/setup"
       element={
         <ProtectedRoute>
           <AssessmentSetupPage />
         </ProtectedRoute>
       }
       />

      <Route
      path="/roadmap/assessment/:topicId/exam"
      element={
        <ProtectedRoute>
          <AssessmentExamPage />
        </ProtectedRoute>
      }
      />

      <Route
      path="/roadmap/assessment/:topicId/result"
      element={
        <ProtectedRoute>
          <AssessmentResultPage />
        </ProtectedRoute>
      }
      />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
