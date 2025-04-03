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

  // === 📊 Compute statistics ===
  const now = Date.now();
  const todayCutoff = now - 24 * 60 * 60 * 1000;
  const weekCutoff = now - 7 * 24 * 60 * 60 * 1000;
  const currentMonth = new Date().getMonth();
  const currentYear = new Date().getFullYear();

  let distanceToday = 0;
  let distanceWeek = 0;
  let distanceMonth = 0;
  let totalTimeSeconds = 0;
  let rideCount = 0;

  activities.forEach((act) => {
    let createdTime = act.createdAt?.seconds
      ? act.createdAt.seconds * 1000
      : new Date(act.createdAt).getTime();

    const dist = act.distance || 0;
    const time = act.timeTaken || act.duration || 0;

    if (createdTime >= todayCutoff) {
      distanceToday += dist;
    }
    if (createdTime >= weekCutoff) {
      distanceWeek += dist;
    }

    const actDate = new Date(createdTime);
    if (
      actDate.getMonth() === currentMonth &&
      actDate.getFullYear() === currentYear
    ) {
      distanceMonth += dist;
    }

    totalTimeSeconds += time;
    rideCount += 1;
  });

  const toKm = (m: number) => (m / 1000).toFixed(2);
  const toHours = (s: number) => (s / 3600).toFixed(2);

  return (
    <div className="profile-container">
      <DisplayProfile />

      <div className="cycling-statistics">
        <CyclingStatistics />
        <div className="statistics-list-container">
          <ul className="statistics-list">
            <p>Today: {toKm(distanceToday)} km</p>
            <p>This Week: {toKm(distanceWeek)} km</p>
            <p>This Month: {toKm(distanceMonth)} km</p>
            <p>Total Time: {toHours(totalTimeSeconds)} hrs</p>
            <p>Number of Rides: {rideCount}</p>
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
