import "../pages-css/SavedRoutes.css";
import React, { useEffect, useState } from "react";
import Navigate from "../components/Navigation";
import DisplayProfile from "../components/displayProfile";
import SavedRoute from "../components/SavedRoute";

function SavedRoutes() {
  const [savedRoutes, setSavedRoutes] = useState<any[]>([]);

  useEffect(() => {
    const fetchRoutes = async () => {
      const userUID = sessionStorage.getItem("userUID");
      if (!userUID) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:1234/get-saved-routes?userUID=${userUID}`
        );
        const data = await res.json();

        // Sort by most recent `lastUsedAt`
        const sorted = data.sort((a: any, b: any) => {
          const timeA = a.lastUsedAt?.seconds
            ? a.lastUsedAt.seconds * 1000
            : new Date(a.lastUsedAt || 0).getTime();
          const timeB = b.lastUsedAt?.seconds
            ? b.lastUsedAt.seconds * 1000
            : new Date(b.lastUsedAt || 0).getTime();
          return timeB - timeA; // descending
        });

        setSavedRoutes(sorted);
      } catch (err) {
        console.error("Error fetching saved routes:", err);
      }
    };

    fetchRoutes();
  }, []);

  return (
    <div>
      <DisplayProfile />
      <div className="saved-route-title">
        <h3>Here are your saved routes</h3>
      </div>

      <div className="saved-routes-list">
        {savedRoutes.map((route) => (
          <SavedRoute key={route.id} route={route} />
        ))}
      </div>

      <div className="footer"></div>

      <Navigate />
    </div>
  );
}

export default SavedRoutes;
