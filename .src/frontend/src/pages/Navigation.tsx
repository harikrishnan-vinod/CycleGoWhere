import "../pages-css/Navigate.css";
import React from 'react';


const Navigate = () => {
    return (
        <div className="navigation">
            <ul>
                <li><a href="#home">Main</a></li>
                <li><a href="#profile">Profile</a></li>
                <li><a href="#services">SavedRoutes</a></li>
                <li><a href="#contact">Settings</a></li>
            </ul>
        </div>
    );
};

export default Navigate;
