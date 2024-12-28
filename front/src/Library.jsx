import FileShow from "./components/FileShow.jsx";
import './css/library.css';
import { LuSearch } from "react-icons/lu";
import Navbar from "./components/Navbar.jsx";
import { useEffect, useState } from "react";
import axios from "axios";

function Library() {
    const [subjects, setSubjects] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [allMaterials, setAllMaterials] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        async function getSubjects() {
            try {
                const response = await axios.post("http://127.0.0.1:8000/get-subjects");
                setSubjects(response.data);
                if (response.data.length > 0) {
                    await getMaterials({ target: { value: response.data[0].name } });
                }
            } catch (error) {
                console.log(error);
            }
        }
        getSubjects();
    }, []);

    async function getMaterials(e) {
        const subject = e.target.value;
        try {
            const response = await axios.post("http://127.0.0.1:8000/get-materials", { subject });
            setMaterials(response.data.materials);
            setAllMaterials(response.data.materials);
        } catch (error) {
            console.log(error);
            setMaterials([]);
            setAllMaterials([]);
        }
    }

    function sort(e) {
        const sortType = e.target.value;
        const sortedMaterials = [...materials].sort((a, b) =>
            sortType === 'AtoZ' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)
        );
        setMaterials(sortedMaterials);
        const sortedAllMaterials = [...allMaterials].sort((a, b) =>
            sortType === 'AtoZ' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)
        );
        setAllMaterials(sortedAllMaterials);
    }


    function search(e) {
        setSearchTerm(e.target.value);
        const filteredMaterials = allMaterials.filter(item =>
            item.name.toLowerCase().includes(e.target.value.toLowerCase())
        );
        setMaterials(filteredMaterials);
    }

    return (
        <>
            <Navbar />
            <div className="library">
                <div className="search-table">
                    <div>
                        <div className="course-select">
                            <label className="col-5" style={{ paddingRight: "10px" }}> Course: </label>
                            <select className="course-dropdown col-7" onChange={getMaterials}>
                                {subjects.map((item, index) => <option key={index} value={item.name}>{item.name}</option>)}
                            </select>
                        </div>
                    </div>
                    <div>
                        <div className="course-select">
                            <div className="">
                                <label style={{ paddingRight: "10px" }}> <LuSearch style={{ fontSize: "35px" }} /> </label>
                                <input className="search" type="text" placeholder="Search..." value={searchTerm} onChange={search} />
                            </div>
                        </div>
                    </div>
                    <div>
                        <div className="course-select">
                            <label style={{ paddingRight: "10px" }}> Sort : </label>
                            <select className="course-dropdown" onChange={sort}>
                                <option value="AtoZ">A to Z</option>
                                <option value="ZtoA">Z to A</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div className="data-content">
                    <div className="data-grid row">
                        {materials.map((item, index) => <FileShow key={index} filename={item.name} type={item.type} id={item.id} />)}
                    </div>
                </div>
            </div>
        </>
    );
}

export default Library;
