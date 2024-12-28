import './css/addMaterial.css';
import { BsUpload } from "react-icons/bs";
import Navbar from "./components/Navbar.jsx";
import { useEffect, useState } from "react";
import axios from "axios";

function AddMaterial() {
    const [file, setFile] = useState(null);
    const [subjects, setSubjects] = useState([]);
    const [sub, setSub] = useState('');

    useEffect(() => {
        async function getSubjects() {
            try {
                const response = await axios.post("http://127.0.0.1:8000/get-subjects");
                setSubjects(response.data);
                if (response.data.length > 0) {
                    setSub(response.data[0].name);
                }
            } catch (error) {
                console.log(error);
            }
        }
        getSubjects();
    }, []);

    async function addMaterial() {
        if (!file || !sub) {
            console.log("All fields are required.");
            return;
        }

        const formData = new FormData();
        formData.append('subject', sub);
        formData.append('file', file);

        try {
            const response = await axios.post("http://127.0.0.1:8000/add-material", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    }

    function fileChange(event) {
        setFile(event.target.files[0]);
    }

    return (
        <>
            <Navbar />
            <div className="add-material">
                <div className="select-course course-select col-6">
                    <label className={"col-4"}>Select Course</label>
                    <select className={"col-6 course-dropdown"} value={sub} onChange={(e) => setSub(e.target.value)}>
                        {subjects.map((item, index) => <option key={index} value={item.name}>{item.name}</option>)}
                    </select>
                </div>

                <div className={"submit-btn"}>
                    <button className={"add-material-btn btn btn-lg col-2 "} onClick={addMaterial}>Submit</button>
                </div>
                <div>
                    <div className={"file-input-div col-4"}>
                        <label className={"file-label"} htmlFor={"file"}><BsUpload /></label>
                        <input
                            id={"file"}
                            type={"file"}
                            className={"file-input col-4"}
                            accept=".pdf,.png,.jpeg,.jpg,.pptx,.ppt"
                            onChange={fileChange}
                            multiple={false}
                        />
                    </div>
                </div>
            </div>
        </>
    );
}

export default AddMaterial;
