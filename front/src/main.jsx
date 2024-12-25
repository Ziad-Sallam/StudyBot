import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './main.css'
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import LogIn from "./LogIn.jsx";
import ChatBox from "./components/chatBox.jsx";
import Library from "./Library.jsx";
import AddMaterial from "./AddMaterial.jsx";
import axios from "axios";



const router = createBrowserRouter([
    {
        path: '/',
        element: <LogIn />
    },

    {
        path: '/:user/:token',
        element: <App />,
    },
    {
        path: '/:user/:token/library',
        element: <Library/>
    },
    {
        path: '/:user/:token/addMaterial',
        element: <AddMaterial/>
    }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
