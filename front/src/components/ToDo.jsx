import 'react-resizable/css/styles.css';
import ToDoItem from './ToDoItem.jsx'
import {useEffect, useState} from "react";
import propTypes from 'prop-type'
import axios from "axios";


ToDo.propTypes ={
    todo: propTypes.list
}


function ToDo(){
    const [size,setSize] = useState({ width: window.innerWidth *0.25, height: window.innerHeight });
    addEventListener('resize', ()=>{
        setSize((prevState) => {
                return {width: window.innerWidth * 0.25, height: prevState.height };
            }
        );
    })
    const [todo,setTodo] = useState([])

    useEffect(() => {
        const getTodo = async () =>{
            try{
                const response = await axios.post("http://127.0.0.1:8000/get-assignments")
                setTodo(response.data.assignments)
                console.log("look here :")
                console.log(response.data.assignments)
                console.log(todo)
            }catch(error){
                console.log(error)
            }

        }
        getTodo()
        const interval = setInterval(getTodo, 3000);
        return () => clearInterval(interval);
    },[todo])

    return (
        <div className="row todo-list">
            <div>

                    {todo.map((item, index) =>
                        <ToDoItem
                            key={index}
                            item={item}
                        />
                    )}
            </div>


        </div>

    )
}

export default ToDo;