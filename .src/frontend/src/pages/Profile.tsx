import Navigate from "../components/Navigation";
import "../pages-css/Profile.css";
import DisplayProfile from "../components/displayProfile";
import CyclingActivity from "../components/CyclingActivity";
import CyclingStatistics from "../components/CyclingStatistics";
import { Link } from "react-router-dom";
import next from "../assets/next.png";

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
        <div className="pb-container">
          Personal Best:
          <Link to="/PersonalBest">
            <img src={next} />
          </Link>
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
