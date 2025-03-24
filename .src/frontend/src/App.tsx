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

import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate replace to="/login" />} />
        <Route path="/MainPage" element={<MainPage />} />
        <Route path="/Profile" element={<Profile />} />
        <Route path="/SavedRoutes" element={<SavedRoutes />} />
        <Route path="/Settings" element={<Settings />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/hangeUsername" element={<ChangeUsername />} />
        <Route path="/ChangeEmail" element={<ChangeEmail />} />
        <Route path="/ChangePassword" element={<ChangePassword />} />
        <Route
          path="/changeProfilePicture"
          element={<ChangeProfilePicture />}
        />
      </Routes>
    </Router>
  );
}

export default App;
