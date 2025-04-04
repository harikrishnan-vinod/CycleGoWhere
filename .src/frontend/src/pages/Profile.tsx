import { useEffect, useState } from "react";
import Navigate from "../components/Navigation";
import "../pages-css/Profile.css";
import DisplayProfile from "../components/displayProfile";
import CyclingStatistics from "../components/CyclingStatistics";
import CyclingActivity from "../components/CyclingActivity";

function Profile() {
  const [activities, setActivities] = useState<any[]>([]);

  useEffect(() => {
    const fetchActivities = async () => {
      const userUID = sessionStorage.getItem("userUID");
      if (!userUID) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:1234/get-activities?userUID=${userUID}`
        );
        if (!res.ok) throw new Error("Failed to get activities");
        let data = await res.json();

        data.sort((a: any, b: any) => {
          const getTime = (entry: any) => {
            if (entry.createdAt?.seconds) {
              return entry.createdAt.seconds * 1000;
            }
            if (entry.createdAt) {
              return new Date(entry.createdAt).getTime();
            }
            return 0;
          };
          return getTime(b) - getTime(a);
        });

        setActivities(data);
      } catch (err) {
        console.error("Error fetching activities:", err);
      }
    };

    fetchActivities();
  }, []);


  return (
    <div className="profile-container">
      <DisplayProfile />

      <div className="cycling-statistics">
        <CyclingStatistics />
      </div>
      <div className="activities-list">
        {activities.map((activity) => (
          <CyclingActivity key={activity.id} activity={activity} />
        ))}
      </div>

      <div className="footer">

      </div>
      <Navigate />
    </div>

  );
}

export default Profile;
