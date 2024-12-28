
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import './css/login.css'
import {useNavigate} from 'react-router-dom'
import {useState} from "react";
import axios from "axios";

function LogIn() {
    const navigate = useNavigate();
    function handleEntryChange(e) {
        if (e.target.id === "inputEmail"){
            setEmail(e.target.value)

        }
        else if (e.target.id === "inputPassword"){
            setPassword(e.target.value)
        }
    }
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')


    async function handleLogin(e) {
        const params = {
            username: email,
            password: password,
        };

        e.preventDefault();

        console.log(email);
        console.log(password);
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/token/", params);
            console.log(response.data);
            const user = response.headers.authorization;
            console.log(user)
            window.sessionStorage.setItem("token", JSON.stringify(user));
            window.sessionStorage.setItem("is_admin",JSON.stringify(response.headers.is_admin))
            navigate(`/${email}`)


        } catch (error) {
            console.error('There was an error logging in:', error);
        }

    }

    return (
        <>
            <div className={"login-container"}>
                <form className="form-signin" onSubmit={handleLogin}>
                    {/*<img className="mb-4" src={r} alt="" width="72"*/}
                    {/*     height="72"/>*/}
                    <div className={"logo"}>Trixie</div>
                    <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
                    {/*<label htmlFor="inputEmail" className="sr-only">Email address</label>*/}
                    <input type="text" id="inputEmail" className="form-control" placeholder="Username..." required
                           autoFocus value={email} onChange={handleEntryChange}/>
                    {/*<label htmlFor="inputPassword" className="sr-only">Password</label>*/}
                    <input type="password" id="inputPassword" className="form-control last" placeholder="Password" required value={password}
                           onChange={handleEntryChange}/>
                    <button className="btn btn-lg btn-block col-12 sign-btn" type="submit">Sign in</button>
                </form>
            </div>
        </>
    )

}

export default LogIn