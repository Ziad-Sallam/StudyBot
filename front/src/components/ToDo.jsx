import { ResizableBox } from 'react-resizable';
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
            <div className="col-4" >
                <ResizableBox width={size.width} maxConstraints={[window.innerWidth ]} minConstraints={[300 ]}>
                <table className="list-group" >
                    <tbody>
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
                </ResizableBox>

            </div>
        </div>


    )
}

export default ToDo;