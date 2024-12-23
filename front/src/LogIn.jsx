
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
            email: email,
            password: password,
        };
        navigate(`/${params.email}`)
        e.preventDefault();

        console.log(email);
        console.log(password);
        try {
            const response = await axios.get("http://localhost:8080/api/users/signin", {
                params: { ...params }
            });
            console.log(response.data);
            const user = response.data

            // Optionally navigate after successful login



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
                    <input type="email" id="inputEmail" className="form-control" placeholder="Email address" required
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