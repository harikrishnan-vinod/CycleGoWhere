import { useNavigate } from "react-router-dom";
import "../components-css/changeEmail.css";


function changeEmail() {
    const navigate = useNavigate();

    return <div>

        <div>
            <header>EMAIL</header>
        </div>
        <div>
            <form>
                <ul className="change-email">
                    <li>
                        <input type="text" placeholder="New Email" className="new-Email" required />
                    </li>
                    <li>
                        <input type="text" placeholder="Confirm New Email" className="new-email" required />
                    </li>
                    <button type="submit" className="submit-btn">Change Email</button>
                    <button onClick={() => navigate("/Settings")} type="button" className="cancel-btn">
                        Cancel
                    </button>
                </ul>
            </form>
        </div>
    </div >
}

export default changeEmail;
