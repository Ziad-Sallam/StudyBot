import PropTypes from "prop-types";
import '../css/notifications.css'
import axios from "axios";
import {useEffect, useState} from "react";

Notifications.propTypes = {
    notifications: PropTypes.arrayOf(PropTypes.shape({
        title: PropTypes.string,
        description: PropTypes.string,
    }))
}

function Notifications() {

    const [seen,setSeen] = useState([])

    useEffect(() => {
        const getTodo = async () =>{
            try{
                const response = await axios.post("http://127.0.0.1:8000/get-assignments")
                const data = response.data.assignments
                const x = data.filter(item=>!(item.seen))
                console.log(x)
                setSeen(x)
                const ids = seen.map(item=>item.id)
                const response1 = await axios.post("http://127.0.0.1:8000/set-seen",{idList:ids})
                console.log(response1.data)
                console.log(response.data)


            }catch(error){
                console.log(error)
            }

        }
    getTodo()
    },[])

    return (
        <div className={"notifications-box"}>

            {seen.map((notification,index) => (
                <div key={index} className="notification">
                    <h6 className={"notification-title"}>{notification.subject + " " + notification.type}</h6>

                    <p className="notification-description">{notification.description}</p>
                </div>
            ))}

        </div>
    )
}

export default Notifications;