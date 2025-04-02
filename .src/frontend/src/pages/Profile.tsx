import Navigate from "../components/Navigation";
import "../pages-css/Profile.css";
import DisplayProfile from "../components/displayProfile";
import CyclingActivity from "../components/CyclingActivity";
import CyclingStatistics from "../components/CyclingStatistics";

function Profile() {
  return (
    <div>
      <div>
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
      </div>
      <div className="activities-list">
        <CyclingActivity />
        <CyclingActivity />
        <CyclingActivity />
      </div>

      <div>
        <Navigate />
      </div>
    </div>
  );
}

export default Profile;
