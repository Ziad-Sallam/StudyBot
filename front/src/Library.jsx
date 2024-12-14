import FileShow from "./components/FileShow.jsx";
import './css/library.css'
import {LuSearch} from "react-icons/lu";
import Navbar from "./components/Navbar.jsx";

function Library() {

    return (
    <>
    <Navbar/>
    <div className={"library"}>
        <div className={"search-table"}>
            <div>
                <div className={"course-select"}>
                    <label className={"col-5"} style={{paddingRight: "10px"}}> Course: </label>
                    <select className={"course-dropdown col-7"}>
                        <option value={"HCI"}>HCI</option>
                        <option value={"discrete"}>Discrete</option>
                        <option value={"creative"}>Creative</option>
                    </select>
                </div>

                <div className={"course-select"}>
                    <label className={"col-4"} style={{paddingRight: "10px", paddingTop: "10px"}}> Topic: </label>
                    <select className={"course-dropdown col-8"}>
                        <option value={"HCI"}>All</option>
                        <option value={"discrete"}>visual system</option>
                        <option value={"creative"}>HCI history</option>
                    </select>
                </div>
            </div>
            <div>
                <div className={"course-select"}>
                    <div className={""}>
                        <label style={{paddingRight: "10px"}}> <LuSearch style={{fontSize: "35px"}}/> </label>
                        <input className={"search"} type={"text"} placeholder={"Search..."}/>
                    </div>
                </div>
            </div>
            <div>
                <div className={"course-select"}>
                    <label style={{paddingRight: "10px"}}> Sort : </label>
                    <select className={"course-dropdown"}>
                        <option value={"AtoZ"}>A to Z</option>
                        <option value={"ZtoA"}>Z to A</option>
                        <option value={"date"}>Date Uploaded</option>

                    </select>
                </div>
            </div>


        </div>
        <div className={"data-content"}>
            <div className={"data-grid"}>
                <FileShow filename={"sheet 1"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 2"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 3"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 4"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 5"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 6"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 7"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 8"} date={new Date().toDateString()}/>
                <FileShow filename={"sheet 9"} date={new Date().toDateString()}/>
            </div>
        </div>
    </div>
    </>
)
}

export default Library