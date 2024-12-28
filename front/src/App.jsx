import Navbar from "./components/Navbar.jsx";
import ToDo from "./components/ToDo.jsx";
import ChatBox from "./components/chatBox.jsx";
import './main.css';
import Library from "./Library.jsx";
import AddMaterial from "./AddMaterial.jsx";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useEffect, useState } from "react";
import Task from "./components/Task.jsx";
import { jwtDecode } from "jwt-decode";


function App() {

    const [todo, setTodo] = useState([
        { title: "Todo 1", description: "answers to frequently asked questions", date: '15/11/2024' },
        { title: 'Todo 2', description: "description2", date: '30/11/2024' }
    ]);

    const [tasks, setTasks] = useState([]);
    const token = JSON.parse(window.sessionStorage.getItem('token'));
    const is_admin = JSON.parse(window.sessionStorage.getItem('is_admin'));

    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

    useEffect(() => {
        const fetchData = async () => {
            const x = jwtDecode(token);
            console.log("AAASDASD")
            console.log(x);
            console.log(typeof is_admin)


            try {
                const tasksResponse = await axios.get("http://127.0.0.1:8000/get-tasks");
                setTasks(tasksResponse.data.tasks);
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        fetchData();
    }, [tasks]);

    return (
        <>
            <Navbar />
            <div className="main-page">
                <div>
                    <h3 style={{ color: "white" }}>Assignments:</h3>
                    <ToDo todo={todo} />
                    <Task todo={tasks} />
                </div>
                <ChatBox />
            </div>
        </>
    );
}

export default App;
