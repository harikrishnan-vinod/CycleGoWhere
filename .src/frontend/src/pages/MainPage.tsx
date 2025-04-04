import "../pages-css/MainPage.css";
import Navigate from "../components/Navigation";
import BaseMap from "../components/MapComponents/BaseMap";
function MainPage() {
  return (
    <div>
      <Navigate />
      <BaseMap />
    </div>
  );
}

export default MainPage;
