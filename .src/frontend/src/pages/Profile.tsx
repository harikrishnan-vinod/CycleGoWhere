import Navigate from "../components/Navigation";
import "../pages-css/Profile.css";
import DisplayProfile from "../components/displayProfile";

function Profile() {
  return <div>
    <div>
      <DisplayProfile />
    </div>
    <div>
      <h1>Profile Page</h1>
      <Navigate />
    </div>
  </div>;
}

export default Profile;
