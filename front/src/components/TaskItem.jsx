import PropTypes from "prop-types";
import "../css/todo.css"
import {useState} from "react";
import {CiTrash} from "react-icons/ci";
import axios from "axios";

TaskItem.propTypes ={
    title:PropTypes.string,
    description:PropTypes.string,
    date:PropTypes.string
}


function TaskItem(props) {
    async function deleteTask(){
        console.log(props)
        try{
            const params = {
                id : props.id,
            }
            const response = await axios.post("http://127.0.0.1:8000/delete-task", params)
            console.log(response.data)
        }catch (error){
            console.log(error)
        }
    }
    return (
        <div className={"todo-item todo-item-off" }>

            <div className="ms-2 me-auto add-task">
                <div className="fw-bold text-white">{props.description}</div>
                <button className={"btn"}><CiTrash  style={{color:'white', fontSize: "30px"}} onClick={deleteTask}/></button>

            </div>

        </div>
    )

}

export default TaskItem;