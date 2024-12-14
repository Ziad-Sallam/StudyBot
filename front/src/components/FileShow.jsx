import { FaFile } from "react-icons/fa";
import {PropTypes} from 'prop-types';

FileShow.propTypes = {
    filename: PropTypes.string,
    date: PropTypes.string,
}


function FileShow(props) {

    return (
        <div className={"file-show"}>
            <div className="data-file">
                <FaFile/>
            </div>
            <p className={"file-name"}>{props.filename}</p>
            <p className={"file-date"}>{props.date}</p>
        </div>
    )
}

export default FileShow;