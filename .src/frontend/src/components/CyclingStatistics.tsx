import savedroutesicon from "../assets/savedroutesicon.png";
import deleteicon from "../assets/delete.png";
import "../components-css/CyclingStatistics.css";
import { useEffect, useState } from "react";
import { Camera } from "lucide-react";
import { Link } from "react-router-dom";

function CyclingStatistics() {
    const [username, setUsername] = useState<string | null>(null);

    useEffect(() => {
        const displayUsername = async () => {
            const userUID = sessionStorage.getItem("userUID");
            if (!userUID) return;

            try {
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

        displayUsername();
    }, []);


    return (
        <div className="activity-container">
            <div className="top-activity">
                <div className="profile-details">
                    {username && (
                        <div className="username-title">
                            {username}
                        </div>)}
                </div>
                <div className="date-time">

                </div>
            </div>
            <div className="map-activity">

            </div>
            <div className="activity-statistics">
                <div className="distance">
                    <p>Distance: </p>
                </div>
                <div className="duration">
                    <p>Duration: </p>
                </div>
                <div className="average-speed">
                    <p>Average Speed: </p>
                </div>
            </div>
            <div className="actions-activity">
                <div className="save-activity">
                    <img src={savedroutesicon} alt="Saved Routes" />
                </div>
                <div className="delete-activity">
                    <img src={deleteicon} alt="Delete Routes" /> </div>
            </div>


        </div>
    );
}

export default CyclingStatistics;