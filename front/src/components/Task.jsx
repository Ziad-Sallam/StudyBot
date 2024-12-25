import 'react-resizable/css/styles.css';
import ToDoItem from './ToDoItem.jsx'
import {useState} from "react";
import propTypes from 'prop-type'
import TaskItem from "./TaskItem.jsx";
import AddTask from "./AddTask.jsx";
import {IoAdd} from "react-icons/io5";


Task.propTypes ={
    todo: propTypes.list
}


function Task(props){
    const [add,setAdd] = useState(false)




    function formatDate(dateString) { // Create a new Date object from the input string
        const date = new Date(dateString); // Extract the date parts
        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        const day = String(date.getUTCDate()).padStart(2, '0'); // Return the formatted date (YYYY-MM-DD)
        return `${year}-${month}-${day}`;
    }



    return (
        <div className="row todo-list">
            <div>

                <div className="add-task">
                    <h3 style={{color: "white"}}>Tasks:</h3>
                    <button className={"btn"} onClick={()=> setAdd(!add)}><IoAdd style={{color:"green", fontSize: "30px"}}/></button>
                </div>

                {add && <AddTask/>}
                {props.todo.map((item, index) =>
                    <TaskItem
                        key={index}
                        title={item.subject + " " + item.type}
                        description={item.description}
                        date={formatDate(item.deadline)}
                        id={item.id}
                    />
                )}
            </div>


        </div>

    )
}

export default Task;