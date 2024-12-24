import 'react-resizable/css/styles.css';
import ToDoItem from './ToDoItem.jsx'
import {useState} from "react";
import propTypes from 'prop-type'


ToDo.propTypes ={
    todo: propTypes.list
}


function ToDo(props){
    const [size,setSize] = useState({ width: window.innerWidth *0.25, height: window.innerHeight });
    addEventListener('resize', ()=>{
        setSize((prevState) => {
                return {width: window.innerWidth * 0.25, height: prevState.height };
            }
        );
    })



    function formatDate(dateString) { // Create a new Date object from the input string
        const date = new Date(dateString); // Extract the date parts
        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        const day = String(date.getUTCDate()).padStart(2, '0'); // Return the formatted date (YYYY-MM-DD)
        return `${year}-${month}-${day}`;
    }



    return (
        <div className="row todo-list">

            <table className="list-group">
                <tbody style={{borderRadius: "20px"}}>
                {props.todo.map((item,index) =>
                    <ToDoItem
                        key={index}
                        title={item.subject}
                        description={item.type}
                        date={formatDate(item.deadline)}
                    />
                )}
                </tbody>

            </table>



        </div>

    )
}

export default ToDo;