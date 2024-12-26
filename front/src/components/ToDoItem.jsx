import PropTypes from "prop-types";
import "../css/todo.css"
import {useEffect, useState} from "react";
import axios from "axios";

ToDoItem.propTypes ={
    title:PropTypes.string,
    description:PropTypes.string,
    date:PropTypes.string
}


function ToDoItem(props) {
    const [on, setOn] = useState(false);
    const [isDone,setIsDone] = useState(props.item.status==="Submitted");

    console.log("here:---")
    console.log(props.item.status)
    console.log(isDone)
    useEffect(() => {
        function x(){
            console.log("hello from the other side");
            console.log(props.item.status);
            setIsDone(props.item.status==="Submitted");

        }
        x()

    },[])

    function formatDate(dateString) { // Create a new Date object from the input string
        const date = new Date(dateString); // Extract the date parts
        console.log("hello")
        console.log(props)
        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        const day = String(date.getUTCDate()).padStart(2, '0'); // Return the formatted date (YYYY-MM-DD)
        return `${year}-${month}-${day}`;
    }

    function onToggle() {
        setOn(!on);
    }
    async function changeStatus(){
        console.log("changeStatus");

        if(isDone === false){
            const response = await axios.post('http://127.0.0.1:8000/complete-assignment',{id:props.item.id})
            console.log(response.data)
            setIsDone(true)

        }else{
            const response = await axios.post('http://127.0.0.1:8000/uncomplete-assignment',{id:props.item.id})
            console.log(response.data)
            setIsDone(false)
        }

    }

    return (
        <div className={"todo-item " + (on? "todo-item-on" :"todo-item-off")} onClick={onToggle}>
            <table className="list-group">
                <tbody>
                <tr className=" d-flex justify-content-between align-items-start">
                    <th>
                        <div className="ms-2 me-auto">
                            <div className="form-check form-check-inline">
                                <input className="form-check-input me-1 check" type="checkbox" checked={isDone}
                                       id={props.item.id} onChange={changeStatus}/>
                                <div className={"fw-bold text-white "+ (isDone?"crossed": "")} >{props.item.subject + " " + props.item.type}</div>

                            </div>
                        </div>
                    </th>
                    <th className="table-responsive-lg">
                        <div className="ms-2 me-auto text-white">
                            {formatDate(props.item.deadline)}
                        </div>
                    </th>

                </tr>
                </tbody>

            </table>
            {on && <div className="fw-medium text-white">{props.item.description}</div>}

        </div>
    )

}

export default ToDoItem;