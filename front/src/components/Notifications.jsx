import PropTypes from "prop-types";
import '../css/notifications.css'

Notifications.propTypes = {
    notifications: PropTypes.arrayOf(PropTypes.shape({
        title: PropTypes.string,
        description: PropTypes.string,
    }))

}

function Notifications(props) {

    return (
        <div className={"notifications-box"}>

            {props.notifications.map((notification,index) => (
                <div key={index} className="notification">
                    <h6 className={"notification-title"}>{notification.title}</h6>
                    <hr/>
                    <p className="notification-description">{notification.description}</p>
                </div>
            ))}

        </div>
    )
}

export default Notifications;