import { useNavigate } from "react-router-dom";
import "../components-css/changePassword.css";
import { useState } from "react";


function changePassword() {
    return <div>

        <div>
            <header>CHANGE PASSWORD</header>
        </div>
        <div>
            <form>
                <ul className="change-password">
                    <li>
                        <input type="text" placeholder="New Password" className="new-password" required />
                    </li>
                    <li>
                        <input type="text" placeholder="Confirm New Password" className="new-password" required />
                    </li>
                    <button type="submit" className="submit-btn">Change Password</button>
                    <button onClick={() => navigate("/Settings")} type="button" className="cancel-btn">
                        Cancel
                    </button>
                </ul>
            </form>
        </div>
    </div >
}

export default changePassword;
