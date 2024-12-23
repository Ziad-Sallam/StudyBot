

import Navbar from "./components/Navbar.jsx";
import ToDo from "./components/ToDo.jsx";
import ChatBox from "./components/chatBox.jsx";
import LogIn from "./LogIn.jsx";
import './main.css'
import Library from "./Library.jsx";
import AddMaterial from "./AddMaterial.jsx";

function App() {

    var todo=[
        {title:"Todo 1", description:"answers to a frequently asked questions", date: '15/11/2024'},
        {title: 'Todo 2', description: "description2", date: '30/11/2024'}


    ]


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