import '../css/addWssignmentWidget.css'
import {useEffect, useState} from "react";
import axios from "axios";


function AddAssignmentWidget() {

    const [subjects, setSubjects] = useState([])
    const [sub,setSub] = useState('')
    const [type, setType] = useState('Sheet')
    const [description, setDescription] = useState('')
    const [date, setDate] = useState(null)

    async function handleSubmit() {
        try {


            const params = {
                deadline: date,
                subject: sub,
                type: type,
                description: description,
            }
            console.log(params)

            const response = await axios.post("http://127.0.0.1:8000/create-assignment",params)
            console.log(response.data)

        }catch (error){
            console.log(error)
        }

    }

    useEffect(() =>{
        async function getSubjects(){
            try{
                const response = await axios.post("http://127.0.0.1:8000/get-subjects");
                setSubjects(response.data)
                setSub(response.data.at(0).name)
            }
            catch(error){
                console.log(error)
            }
        }

        getSubjects();

    },[])


    return (
        <div className={"add-assignment-widget-container"}>
            <table className={"add-assignment-widget"}>
                <tbody>
                <tr>
                    <th><label>subject</label></th>
                    <th><select name="subject" id="subject" value={sub} onChange={(e) => setSub(e.target.value)}>
                        {subjects.map((item, index) => {
                            return (<option key={index} value={item.name}>{item.name}</option>)
                        })}

                    </select>
                    </th>


                </tr>
                <tr>
                    <th><label>Type: </label></th>
                    <th>
                        <select name="type" id="type" value={type} onChange={(e) => setType(e.target.value)}>
                            <option value="Sheet">Sheet</option>
                            <option value="Quiz">Quiz</option>
                            <option value="Lab">Lab</option>
                            <option value="Custom">Custom</option>
                        </select>
                    </th>

                </tr>
                <tr>
                    <th><label>Deadline: </label></th>
                    <th><input type={"date"} value={date} onChange={(e) => {
                        setDate(e.target.value)
                        console.log(typeof date)
                    }}/></th>

                </tr>
                <tr>
                    <th><label>Description: </label></th>
                    <th><input type={"text"} value={description} onChange={(e) => setDescription(e.target.value)}/></th>
                </tr>
                </tbody>

            </table>
            <button className={"btn btn-outline-light"} onClick={handleSubmit}>Submit</button>
        </div>

    )

}

export default AddAssignmentWidget