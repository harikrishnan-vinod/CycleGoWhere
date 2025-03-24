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
      <ul className="settings-options">
        <li>
          <button onClick={() => navigate("/changeUsername")}>
            Change Username
          </button>
        </li>
        <li>
          <button onClick={() => navigate("/changeEmail")}>
            Change Email
          </button>
        </li>
        <li>
          <button onClick={() => navigate("/changePassword")}>
            Change Password
          </button>
        </li>
        <li>
          <button onClick={() => navigate("/changeProfilePicture")}>
            Change Profile Picture
          </button>
        </li>
      </ul>
    </div >
  );
}

export default Settings;
