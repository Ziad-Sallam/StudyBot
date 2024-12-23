import PropTypes from "prop-types";
import "../css/todo.css"
import {useState} from "react";

ToDoItem.propTypes ={
    title:PropTypes.string,
    description:PropTypes.string,
    date:PropTypes.string
}


function ToDoItem(props) {
    const [on, setOn] = useState(false);

    function onToggle() {
        setOn(!on);
    }
    return (
        <div className={"todo-item " + (on? "todo-item-on" :"todo-item-off")} onClick={onToggle}>
            <table className="list-group">
            <tr className=" d-flex justify-content-between align-items-start">
                <th>
                    <div className="ms-2 me-auto">
                        <div className="form-check form-check-inline">
                            <input className="form-check-input me-1 check" type="checkbox" value=""
                                   id="firstCheckbox"/>

                            <div className="fw-bold text-white">{props.title}</div>


                        </div>
                    </div>
                </th>
                <th className="table-responsive-lg">
                    <div className="ms-2 me-auto text-white">
                        {props.date}
                    </div>
                </th>

            </tr>
            </table>
            {on && <div className="fw-medium text-white">{props.description}</div>}

        </div>
    )

}

export default ToDoItem;