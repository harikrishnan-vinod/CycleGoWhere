import "../pages-css/Settings.css";
import React from "react";
import { useNavigate } from "react-router-dom";
import Navigate from "../components/Navigation";

function Settings() {
  const navigate = useNavigate();

  return (
    <div>
      <header>
        SETTINGS
      </header>
      <button className="logout-button" onClick={() => navigate("/logout")}>
        Log Out
      </button>
      <Navigate />
      <div className="settings-options">
        <button className="change" onClick={() => navigate("/changeUsername")}>
          Change Username
        </button>
        <button className="change" onClick={() => navigate("/changeEmail")}>
          Change Email
        </button>
        <button className="change" onClick={() => navigate("/changePassword")}>
          Change Password
        </button>
        <button className="change" onClick={() => navigate("/changeProfilePicture")}>
          Change Profile Picture
        </button>
      </div>
    </div>
  );
}

export default Settings;
