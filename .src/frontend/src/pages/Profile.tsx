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
        console.log("Activities fetched:", data);

        data.sort((a: any, b: any) => {
          const tA = a.createdAt?.seconds || 0;
          const tB = b.createdAt?.seconds || 0;
          return tB - tA;
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
        <div className="statistics-list-container">
          <ul className="statistics-list">
            <p>Today: </p>
            <p>This Week:</p>
            <p>This Month:</p>
            <p>Total Time</p>
            <p>Number of Rides:</p>
          </ul>
        </div>
      </div>

      <div className="activities-list">
        {activities.map((activity) => (
          <CyclingActivity key={activity.id} activity={activity} />
        ))}
      </div>

      <Navigate />
    </div>
  );
}

export default Profile;
