import "../pages-css/Settings.css";
import React from "react";
import { useNavigate } from "react-router-dom";
import Navigate from "../components/Navigation";

function Settings() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Settings</h1>
      <button className="logout-button" onClick={() => navigate("/logout")}>
        Log Out
      </button>
      <Navigate />
    </div>
  );
}

export default Settings;
