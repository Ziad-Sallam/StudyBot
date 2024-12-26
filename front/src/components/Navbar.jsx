import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import NotificationsIcon from '@mui/icons-material/Notifications';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min'
import {useParams} from "react-router-dom";
import {useState} from "react";
import Notifications from "./Notifications.jsx";
import {CiLogout} from "react-icons/ci";

function Navbar() {
    const params = useParams();

    const [notification,setNotification] = useState(false);
    const notify = [
        {
        title: "New HCI assignment",
        description: "check your todo list ",
        },
        {
            title: "Example",
            description: "this is an example",
        },
        {
            title: "Lecture canceled",
            description: "tomorrow’s numerical lecture has postponed",
        },
    ]

    return (

        <nav className="navbar navbar-expand-lg navbar-light bg-transparent">
            <div className="container-fluid">
                <a className="navbar-brand logo" href={`/${params.user}/${params.token}`} >Trixie</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="true"  aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <div className="navbar-nav">

                        <li className="nav-item">
                            <a className="nav-link" href={`/${params.user}/${params.token}/addMaterial`}>Add
                                Material</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={`/${params.user}/${params.token}/library`}>Library</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" onClick={() => setNotification(!notification)}><NotificationsIcon
                                color={"inhert"}/>Notification</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link"><AccountCircleIcon/>{params.user}</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href={"/"}><CiLogout />Log Out</a>
                        </li>
                    </div>
                </div>

            </div>
            {notification && (<Notifications/>)}
        </nav>
    )
}

export default Navbar;