import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;