import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Camera } from "lucide-react";

const DisplayProfile: React.FC = () => {
    const navigate = useNavigate();
    const [profilePicUrl, setProfilePicUrl] = useState<string | null>(null);

    // Fetch the profile picture when the component mounts
    useEffect(() => {
        const displayProfilePicture = async () => {
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

        displayProfilePicture();
    }, []); // Empty dependency array ensures this runs only once when the component mounts

    return (
        <div className="profile-pic-content">
            {profilePicUrl ? (
                <div className="profile-image-preview-container">
                    <img
                        src={profilePicUrl}
                        alt="Profile"
                        className="profile-image-preview"
                    />
                </div>
            ) : (
                <div className="profile-image-preview-container">
                    <Camera size={24} />
                </div>
            )}
        </div>
    );
};

export default DisplayProfile;
