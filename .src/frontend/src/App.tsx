import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import MainPage from "./pages/MainPage";
import Login from "./pages/Login";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import SavedRoutes from "./pages/SavedRoutes";
import Register from "./pages/Register";
import Logout from "./components/Logout";
import ChangeUsername from "./components/ChangeUsername";
import ChangeEmail from "./components/ChangeEmail";
import ChangePassword from "./components/ChangePassword";
import ChangeProfilePicture from "./components/ChangeProfilePicture";

import ProtectedRoute from "./components/ProtectedRoute"; // ✅ import the wrapper
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate replace to="/login" />} />

        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes */}
        <Route
          path="/MainPage"
          element={
            <ProtectedRoute>
              <MainPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/SavedRoutes"
          element={
            <ProtectedRoute>
              <SavedRoutes />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route
          path="/logout"
          element={
            <ProtectedRoute>
              <Logout />
            </ProtectedRoute>
          }
        />
        <Route
          path="/changeUsername"
          element={
            <ProtectedRoute>
              <ChangeUsername />
            </ProtectedRoute>
          }
        />
        <Route
          path="/ChangeEmail"
          element={
            <ProtectedRoute>
              <ChangeEmail />
            </ProtectedRoute>
          }
        />
        <Route
          path="/ChangePassword"
          element={
            <ProtectedRoute>
              <ChangePassword />
            </ProtectedRoute>
          }
        />
        <Route
          path="/changeProfilePicture"
          element={
            <ProtectedRoute>
              <ChangeProfilePicture />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
