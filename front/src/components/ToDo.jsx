import { ResizableBox } from 'react-resizable';
import 'react-resizable/css/styles.css';
import ToDoItem from './ToDoItem.jsx'
import {useState} from "react";


function ToDo(){
    const [size] = useState({ width: window.innerWidth *0.25, height: window.innerHeight });


    return (

        <div className="row todo-list">
            <div className="col-4" >
                <ResizableBox width={size.width}>
                <table className="list-group" >


                    <ToDoItem
                        title="To Do 1"
                        description="description1"
                    />
                    <ToDoItem
                        title="To Do 2"
                        description="description2"
                    />
                    <ToDoItem
                        title="To Do 3"
                        description="description2"
                    />

                </table>
                </ResizableBox>

            </div>
        </div>


    )
}

export default ToDo;