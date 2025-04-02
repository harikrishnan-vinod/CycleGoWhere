import { useEffect, useState } from "react";
import { Camera } from "lucide-react";
import { Link } from "react-router-dom";

import "../components-css/displayProfile.css";

const DisplayProfile: React.FC = () => {
    const [profilePicUrl, setProfilePicUrl] = useState<string | null>(null);
    const [username, setUsername] = useState<string | null>(null);

    useEffect(() => {
        const displayProfileData = async () => {
            const userUID = sessionStorage.getItem("userUID");
            if (!userUID) return;

            try {
                // Fetch profile picture
                const profilePicResponse = await fetch(
                    `http://127.0.0.1:1234/get-profile-pic?userUID=${userUID}`
                );
                const profilePicResult = await profilePicResponse.json();

                if (profilePicResponse.ok && profilePicResult.profilePic) {
                    setProfilePicUrl(profilePicResult.profilePic);
                }

                // fetch username
                const usernameResponse = await fetch(
                    `http://127.0.0.1:1234/get-username?userUID=${userUID}`
                );
                const usernameResult = await usernameResponse.json();

                if (usernameResponse.ok && usernameResult.username) {
                    setUsername(usernameResult.username);
                }
            } catch (err) {
                console.error("Error fetching profile data:", err);
            }
        };

        displayProfileData();
    }, []);

    return (
        <div className="profile-pic-content">
            <div className="profile-header">
                {profilePicUrl ? (
                    <div className="profile-image-preview-container">
                        <Link to="/Profile">
                            <img
                                src={profilePicUrl}
                                alt="Profile"
                                className="profile-image-preview"
                            />
                        </Link>
                    </div>
                ) : (
                    <div className="profile-image-preview-container">
                        <Camera size={24} />
                    </div>
                )}

                {username && (
                    <div className="username-title">
                        Welcome, {username}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DisplayProfile;
