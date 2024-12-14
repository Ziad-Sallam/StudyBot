import './css/addMaterial.css'
import {BsUpload} from "react-icons/bs";
import Navbar from "./components/Navbar.jsx";


function AddMaterial() {
    return (
        <>
        <Navbar/>
        <div className="add-material">
            <div className="select-course course-select col-6">
                <label className={"col-4"}>Select Course</label>
                <select className={"col-6 course-dropdown"} e>
                    <option>HCI</option>
                    <option>discrete</option>
                    <option>numerical analysis</option>
                </select>
            </div>
            <div className={"name-select course-select col-6"}>

                <label className={"col-4 "}>File Name</label>
                <input className={"search col-6"} type={"text"} placeholder={"Name..."}/>

            </div>
            <div className={"topic-select col-6 course-select"}>
                <label className={"col-4"}>Topic</label>
                <input className={"search col-6"} type={"text"} placeholder={"Topic..."}/>
            </div>
            <div className={"submit-btn"}>
                <button className={"add-material-btn btn btn-lg col-2 "} onClick={AddMaterial}>Submit</button>
            </div>
            <div>
                <div className={"file-input-div col-4"}>
                    <label className={"file-label"} htmlFor={"file"}><BsUpload/></label>
                    <input id={"file"} type={"file"} className={"file-input col-4"} placeholder={"adddd"}/>

                </div>
            </div>


        </div>
        </>
    )
}

export default AddMaterial;