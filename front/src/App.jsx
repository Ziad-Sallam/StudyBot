
import './main.css'
import Navbar from "./components/Navbar.jsx";
import ToDo from "./components/ToDo.jsx";

function App() {

    var todo=[
        {title:"todo1", description:"description1", date: '15/11/2024'},
        {title: 'todo2', description: "description2", date: '30/11/2024'}


    ]




  return (
    <>
      <Navbar/>
        <ToDo
            todo={todo}
        />
    </>
  )
}

export default App
