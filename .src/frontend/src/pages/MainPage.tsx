import "../pages-css/MainPage.css";
import React from "react";
import Navigate from "../components/Navigation";
import BaseMap from "../components/MapComponents/BaseMap";
function MainPage() {
  return (
    <div>
      <h1>Main Page</h1>
      <Navigate />
      <BaseMap />
    </div>
  );
}

export default MainPage;
