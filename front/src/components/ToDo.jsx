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

    return (
        <div className="row todo-list">

            <table className="list-group">
                <tbody style={{borderRadius: "20px"}}>
                {props.todo.map(item =>
                    <ToDoItem
                        key={item.title}
                        title={item.title}
                        description={item.description}
                        date={item.date}
                    />
                )}
                </tbody>

            </table>



        </div>

    )
}

export default ToDo;