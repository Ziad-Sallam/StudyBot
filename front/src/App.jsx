

import Navbar from "./components/Navbar.jsx";
import ToDo from "./components/ToDo.jsx";
import ChatBox from "./components/chatBox.jsx";
import LogIn from "./LogIn.jsx";
import './main.css'
import Library from "./Library.jsx";
import AddMaterial from "./AddMaterial.jsx";
import {useParams} from "react-router-dom";
import axios from "axios";
import {useEffect, useState} from "react";

function App() {

    const params =  useParams();

    const [todo,setTodo]=useState([
        {title:"Todo 1", description:"answers to a frequently asked questions", date: '15/11/2024'},
        {title: 'Todo 2', description: "description2", date: '30/11/2024'}
    ])

    useEffect(() => {
        const getTodo = async () =>{
            try{
                const response = await axios.post("http://127.0.0.1:8000/get-assignments")
                setTodo(response.data.assignments)
                console.log(todo)
            }catch(error){
                console.log(error)
            }
        }
        getTodo()
    },[])
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + params.token;

    return (
        <>
            <Navbar/>
              <div className={"main-page"}>
                  <ToDo
                      todo={todo}
                  />
                  <ChatBox/>
              </div>

        </>
    )
}

export default App