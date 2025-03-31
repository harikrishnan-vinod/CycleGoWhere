import Navigate from "../components/Navigation";
import "../pages-css/Profile.css";
import DisplayProfile from "../components/DisplayProfile";
import CyclingStatistics from "../components/CyclingStatistics";

function Profile() {
  return <div>
    <div>
      <DisplayProfile />
    </div>
    <div>
      <CyclingStatistics />
    </div>

    <div>
      <Navigate />
    </div>
  </div>;
}

export default Profile;
