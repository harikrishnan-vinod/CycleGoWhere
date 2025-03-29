import { useEffect, useState } from "react";
import "../components-css/changeProfilePicture.css";
import { useNavigate } from "react-router-dom";

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
    const username = sessionStorage.getItem("username");
    if (!username) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:1234/get-profile-pic?username=${username}`
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

    const username = sessionStorage.getItem("username");
    if (!username) {
      setError("No username found in sessionStorage");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("username", username);

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
    <div className="change-profile-container">
      <header>PROFILE PICTURE</header>

      {profilePicUrl && (
        <div className="profile-pic-frame">
          <img
            src={profilePicUrl}
            alt="Profile"
            className="profile-image-preview"
          />
        </div>
      )}

      <div className="upload-controls">
        {/* Hidden file input */}
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          style={{ display: "none" }}
        />
        {/* Custom label for file input */}
        <label htmlFor="file-upload" className="custom-file-label">
          {fileChosen ? "File Uploaded" : "Choose File"}
        </label>
        <button
          onClick={handleUpload}
          className={`upload-button ${success ? "success" : ""}`}
        >
          {success ? "Image Uploaded" : "Upload"}
        </button>
        <button
          onClick={() => navigate("/Settings")}
          type="button"
          className="cancel-btn"
        >
          {success ? "Back to Settings" : "Cancel"}
        </button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
    </div>
  );
}

export default ChangeProfilePicture;
