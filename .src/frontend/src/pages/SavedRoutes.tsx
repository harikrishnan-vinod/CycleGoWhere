import "../pages-css/SavedRoutes.css";
import React from 'react';
import { useState } from "react";
import { UserRoundCheck, Lock } from "lucide-react";
import Navigate from "../components/Navigation";
import DisplayProfile from "../components/displayProfile";
import SavedActivity from "../components/SavedActivity";


function SavedRoutes() {
    return <div>
        <div>
            <DisplayProfile />
            <div className="saved-route-title">
                <h2>Here are your saved routes</h2>
            </div>
        </div>
        <div>
            <SavedActivity />
        </div>



        <Navigate />
    </div>;

}

export default SavedRoutes;