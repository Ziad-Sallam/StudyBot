import '../css/addTask.css'
import "../css/todo.css"
import {useState} from "react";
import {TiTick} from "react-icons/ti";
import axios from "axios";


function AddTask() {
    const [task, setTask] = useState('')

    async function handleSubmit() {
        try{
            const params = {
                description: task,
            }
            const response = axios.post("http://127.0.0.1:8000/create-task", params)
            console.log(response.data)
        }catch(error){
            console.log(error)
        }
    }

    return (
        <div className={"todo-item add-task"}>
            <div className={"add-task-input"}>
                <input className={"add-task-input"} type={"text"} placeholder={"add task..."} value={task} onChange={(e) => setTask(e.target.value)}/>
            </div>
            <button className={"btn btn-sm"}><TiTick  style={{color: "green", fontSize: "30px"}} onClick={handleSubmit}/></button>
        </div>
    )
}

export default AddTask;