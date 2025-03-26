import { useNavigate } from "react-router-dom";
import "../components-css/changeUsername.css";


function changeUsername() {
    const navigate = useNavigate();

    return <div>

        <div>
            <header>USERNAME</header>
        </div>
        <div>
            <form>
                <ul className="change-username">
                    <li>
                        <input type="text" placeholder="New Username" className="new-username" required />
                    </li>
                    <li>
                        <input type="text" placeholder="Confirm New Username" className="new-username" required />
                    </li>
                    <button type="submit" className="submit-btn">Change Username</button>
                    <button onClick={() => navigate("/Settings")} type="button" className="cancel-btn">
                        Cancel
                    </button>
                </ul>
            </form>
        </div>
    </div >
}

export default changeUsername;
