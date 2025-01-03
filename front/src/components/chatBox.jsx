import React, { useState } from 'react';
import axios from 'axios';
import AddAssignmentWidget from "./AddAssignmentWidget.jsx";
import CreateNotification from "./CreateNotification.jsx";
import {useNavigate} from "react-router-dom";

function ChatBox() {
    const [mymessage, setMymessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [action, setAction] = useState('');

    const navigate = useNavigate();


    const handleSendClick = async () => {
        if (!mymessage.trim()) return;

        function formatDate(dateString) { // Create a new Date object from the input string
            const date = new Date(dateString); // Extract the date parts
            console.log("hello")

            const year = date.getUTCFullYear();
            const month = String(date.getUTCMonth() + 1).padStart(2, '0');
            const day = String(date.getUTCDate()).padStart(2, '0'); // Return the formatted date (YYYY-MM-DD)
            return `${year}-${month}-${day}`;
        }

        // Add user's message to the screen
        setMymessage('');
        setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: mymessage }]);

        try {
            if(action ==="" || action === "create assignment" || action === "create notification") {
                // Send message to the backend
                const response = await axios.post(
                    'http://127.0.0.1:8000/handle-request',
                    { query: mymessage },
                );

                console.log(response.data);
                // Add bot's response to the screen
                const botReply = response.data.response || 'No response from bot';
                if (botReply === "create task"){
                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "what is the description of this task ?" }]);
                    setAction("create task")

                }
                else if(botReply === "create assignment"){
                    setAction("create assignment")

                } else if(botReply === "create notification"){
                    setAction("create notification")
                } else if(botReply === 'create material'){
                    navigate("./addMaterial");

                } else if(botReply === 'get assignment'){
                    const response = await axios.post("http://127.0.0.1:8000/get-assignments")
                    const assignments = response.data.assignments
                    console.log(assignments)
                    const notDone = assignments.filter((i) => i.status ==="Pending")
                    if(notDone.length ===0){
                        setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "Well done! You've successfully completed all your assignments. Keep up the great work! 🌟📚" }]);
                        return
                    }
                    const sorted = notDone.sort((a, b) => a.deadline.localeCompare(b.deadline));
                    const ans = ("Your Upcoming Assignments:\n\n"+(sorted.map((i,index) => ((index+1)+"."+i.subject+" "+i.type+" " + formatDate(i.deadline) +"\n")))).replaceAll(",","")
                    const f = ans + "\n Wishing you all the best with your tasks! Remember, you're capable of achieving great things! 😊😊"


                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: f }]);

                } else if(botReply === 'get task'){
                    const tasksResponse = await axios.get("http://127.0.0.1:8000/get-tasks");
                    const tasks = tasksResponse.data.tasks
                    console.log(tasks)
                    if(tasks.length ===0){
                        setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "Well done! You've successfully completed all your assignments. Keep up the great work! 🌟📚" }]);
                        return

                    }
                    const ans = ("Your Upcoming Tasks:\n" + tasks.map((i) => "\n" + i.description)).replaceAll(",","")
                    const f = ans + "\n Wishing you all the best with your tasks! Remember, you're capable of achieving great things! 😊😊"

                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: f }]);
                }
                else{
                    const response = await axios.post('http://127.0.0.1:5000',{message:mymessage})
                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: response.data }]);
                    setAction("")
                }

            } else if(action === "create task"){
                const params = {
                    description: mymessage,
                }
                const response = axios.post("http://127.0.0.1:8000/create-task", params)
                console.log(response.data);
                setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "task created successfully! ☺️" }]);
                setAction("")
            }



        } catch (e) {
            console.error('Error:', e);
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: 'bot', text: 'Error' },
            ]);
        }
        // Clear the input field

    };
    function handleClick(e){
        if(e.key === "Enter"){
            handleSendClick()
        }

    }

    return (
        <div className="container mt-5 chat">
            <div
                className="border p-3 chat-box"
                style={{ height: '80%', display: 'flex', flexDirection: 'column' }}
            >
                <div className={"flex-grow-1 overflow-auto mb-3 "}>
                    {messages.map((msg, index) => (
                        <div
                            key={index}

                            style={{
                                display: 'flex',
                                justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                                marginBottom: '10px',
                            }}
                        >
                            <div
                                className={msg.sender === 'user' ? 'user-bubble' : 'bot-bubble'}

                            >
                                {msg.text}
                            </div>
                        </div>
                    ))}
                </div>
                {action === "create assignment" &&<AddAssignmentWidget action={setAction}/>}
                {action === "create notification" && <CreateNotification action={setAction}/>}
                <div className="input-group">
                    <input
                        type="text"
                        value={mymessage}
                        onChange={(e) => setMymessage(e.target.value)}
                        className="form-control"
                        placeholder="Type a message"
                        onKeyDown={handleClick}

                    />
                    <button type="button" onClick={handleSendClick} className="btn btn-primary">
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ChatBox;