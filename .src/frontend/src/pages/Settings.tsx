import "../pages-css/Settings.css";
import React from "react";
import { useNavigate } from "react-router-dom";
import Navigate from "../components/Navigation";
import { User, Mail, Lock, Camera, LogOut } from "lucide-react";
import DisplayProfile from "../components/DisplayProfile";


function Settings() {
  const navigate = useNavigate();

  return (
    <div className="settings-container">
      <div> <DisplayProfile /> </div>
      <div className="settings-header-area">
        <h1 className="settings-title">Settings</h1>
        <button
          className="logout-button"
          onClick={() => navigate("/logout")}
          aria-label="Log out"
        >
          <LogOut size={18} />
          <span>Log Out</span>
        </button>
      </div>

      <div className="settings-card">
        <div className="card-border-top"></div>
        <h2 className="settings-card-title">Account Settings</h2>
        <p className="settings-card-description">
          Manage your account details and preferences
        </p>

        <div className="settings-options">
          <div
            className="settings-option"
            onClick={() => navigate("/changeUsername")}
          >
            <div className="option-icon user">
              <User size={24} />
            </div>
            <div className="option-content">
              <div className="option-title">Change Username</div>
              <div className="option-description">Update your display name</div>
            </div>
          </div>

          <div
            className="settings-option"
            onClick={() => navigate("/changeEmail")}
          >
            <div className="option-icon email">
              <Mail size={24} />
            </div>
            <div className="option-content">
              <div className="option-title">Change Email</div>
              <div className="option-description">
                Update your email address
              </div>
            </div>
          </div>

          <div
            className="settings-option"
            onClick={() => navigate("/changePassword")}
          >
            <div className="option-icon password">
              <Lock size={24} />
            </div>
            <div className="option-content">
              <div className="option-title">Change Password</div>
              <div className="option-description">Update your password</div>
            </div>
          </div>

          <div
            className="settings-option"
            onClick={() => navigate("/changeProfilePicture")}
          >
            <div className="option-icon profile">
              <Camera size={24} />
            </div>
            <div className="option-content">
              <div className="option-title">Change Profile Picture</div>
              <div className="option-description">
                Update your profile image
              </div>
            </div>
          </div>
        </div>
      </div>

      <Navigate />
    </div>
  );
}

export default Settings;
