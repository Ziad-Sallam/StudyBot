import '../css/addWssignmentWidget.css'
import {useEffect, useState} from "react";
import axios from "axios";

function CreateNotification(props) {

    const [title,setTitle] = useState("");
    const [description, setDescription] = useState('')

    async function handleSubmit() {
        try {
            const params = {
                title: title,
                description: description,
            }
            console.log(params)

            const response = await axios.post("http://127.0.0.1:8000/create-notification",params)
            console.log(response.data)
            props.action("")

        }catch (error){
            console.log(error)
        }

    }



    return (
        <div className={"add-assignment-widget-container"}>
            <table className={"add-assignment-widget"}>
                <tbody>

                <tr>
                    <th><label>Title: </label></th>
                    <th><input type={"text"} value={title} onChange={(e) => setTitle(e.target.value)}/></th>
                </tr>
                <tr>
                    <th><label>Description: </label></th>
                    <th><input type={"text"} value={description} onChange={(e) => setDescription(e.target.value)}/></th>
                </tr>
                </tbody>

            </table>
            <button className={"btn btn-outline-light"} onClick={handleSubmit}>Submit</button>
        </div>

    )

}

export default CreateNotification