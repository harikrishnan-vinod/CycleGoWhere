import "../pages-css/SavedRoutes.css";
import React from 'react';
import { useState } from "react";
import { UserRoundCheck, Lock } from "lucide-react";
import Navigate from "../components/Navigation";
import DisplayProfile from "../components/displayProfile";


function SavedRoutes() {
    return <div>
        <div>
            <DisplayProfile />
        </div>
        <div>
            <h1>Saved Routes Page</h1>
            <Navigate />
        </div>
    </div>;

}

export default SavedRoutes;