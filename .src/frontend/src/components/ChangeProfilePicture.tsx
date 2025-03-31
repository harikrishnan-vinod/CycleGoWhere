import { useEffect, useState } from "react";
import "../components-css/changeProfilePicture.css";
import { useNavigate } from "react-router-dom";
import { Camera } from "lucide-react";

function ChangeProfilePicture() {
  const navigate = useNavigate();
  const [image, setImage] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [profilePicUrl, setProfilePicUrl] = useState<string | null>(null);
  const [fileChosen, setFileChosen] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const validTypes = ["image/jpeg", "image/png", "image/jpg", "image/webp"];
    if (!validTypes.includes(file.type)) {
      setError("Only JPG, PNG, or WEBP images are allowed.");
      setImage(null);
      setFileChosen(false);
    } else {
      setError(null);
      setImage(file);
      setFileChosen(true);
    }
  };

  const fetchProfilePicture = async () => {
    const userUID = sessionStorage.getItem("userUID");
    if (!userUID) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:1234/get-profile-pic?userUID=${userUID}`
      );
      const result = await response.json();

      if (response.ok && result.profilePic) {
        setProfilePicUrl(result.profilePic);
      }
    } catch (err) {
      console.error("Failed to fetch profile picture", err);
    }
  };

  useEffect(() => {
    fetchProfilePicture();
  }, []);

  const handleUpload = async () => {
    if (!image) {
      setError("No image selected");
      return;
    }

    const userUID = sessionStorage.getItem("userUID");
    if (!userUID) {
      setError("No userId found in sessionStorage");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("userUID", userUID);

    try {
      const response = await fetch("http://127.0.0.1:1234/upload-profile-pic", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setSuccess("Profile picture updated successfully!");
        setError(null);
        setProfilePicUrl(result.url);
      } else {
        setError(result.message || "Upload failed");
        setSuccess(null);
      }
    } catch (err) {
      setError("Something went wrong");
      setSuccess(null);
    }
  };

  return (
    <div className="profile-pic-container">
      <div className="profile-pic-card">
        <div className="card-border-top"></div>

        <div className="profile-pic-header">
          <div className="profile-pic-icon">
            <Camera size={24} />
          </div>
          <h2 className="profile-pic-title">Change Profile Picture</h2>
        </div>

        <div className="profile-pic-content">
          {profilePicUrl && (
            <div className="profile-image-preview-container">
              <img
                src={profilePicUrl}
                alt="Profile"
                className="profile-image-preview"
              />
            </div>
          )}

          <div className="upload-controls">
            <input
              id="file-upload"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              style={{ display: "none" }}
            />

            <label htmlFor="file-upload" className="file-upload-label">
              {fileChosen ? "File Selected" : "Choose Image"}
            </label>

            <div className="action-buttons">
              <button
                onClick={handleUpload}
                className="submit-button"
                disabled={!image}
              >
                {success ? "Image Uploaded" : "Upload Image"}
              </button>

              <button
                onClick={() => navigate("/Settings")}
                type="button"
                className="cancel-button"
              >
                {success ? "Back to Settings" : "Cancel"}
              </button>
            </div>
          </div>

          {success && <div className="success-message">{success}</div>}

          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    </div>
  );
}

export default ChangeProfilePicture;
