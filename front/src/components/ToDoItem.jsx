import PropTypes from "prop-types";

ToDoItem.propTypes ={
    title:PropTypes.string,
    description:PropTypes.string,
    date:PropTypes.string
}


function ToDoItem(props) {
    return (
        <tr className="list-group-item d-flex justify-content-between align-items-start">
            <th>
            <div className="ms-2 me-auto">
                <div className="form-check form-check-inline">
                    <input className="form-check-input me-1" type="checkbox" value=""
                           id="firstCheckbox"/>

                    <div className="fw-bold">{props.title}</div>

                    <div className="fw-medium">{props.description}</div>
                </div>
            </div>
            </th>
            <th className="table-responsive-lg">
                <div className="ms-2 me-auto">
                    {props.date}
                </div>
            </th>

        </tr>
    )

}
export default ToDoItem;