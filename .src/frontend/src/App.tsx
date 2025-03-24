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
import "./App.css";

function App() {
  return (
    <>
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
        </Routes>
      </Router>
    </>
  );
}

export default App;
