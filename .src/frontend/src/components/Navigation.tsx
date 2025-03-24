import "../components-css/Navigation.css";
import { Link } from "react-router-dom";

import mainpageicon from "../assets/mainpageicon.png";
import profileicon from "../assets/profileicon.png";
import savedroutesicon from "../assets/savedroutesicon.png";
import settingsicon from "../assets/settingsicon.png";

function Navigate() {
  return (
    <div className="navigation">
      <ul className="nav-bar">
        <li className="nav-item">
          <Link to="/MainPage">
            <img src={mainpageicon} alt="Main" />
          </Link>
        </li>

        <li className="nav-item">
          <Link to="/Profile">
            <img src={profileicon} alt="Profile" />
          </Link>
        </li>

        <li className="nav-item">
          <Link to="/SavedRoutes">
            <img src={savedroutesicon} alt="Saved Routes" />
          </Link>
        </li>

        <li className="nav-item">
          <Link to="/Settings">
            <img src={settingsicon} alt="Settings" />
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default Navigate;
