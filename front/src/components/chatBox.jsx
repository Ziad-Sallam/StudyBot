import React, { useState } from 'react';
import axios from 'axios';
import AddAssignmentWidget from "./AddAssignmentWidget.jsx";

function ChatBox() {
    const [mymessage, setMymessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [action, setAction] = useState('');

    const handleSendClick = async () => {
        if (!mymessage.trim()) return;

        // Add user's message to the screen
        setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: mymessage }]);

        try {
            if(action ==="" || action === "create assignment"){
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

                } else if(botReply === "get assignment"){
                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "what is the description of this task ?" }]);

                }
                else if(botReply === "create assignment"){
                    setAction("create assignment")

                }
                else{
                    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botReply }]);
                    setAction("")
                }

            } else if(action === "create task"){
                const params = {
                    description: mymessage,
                }
                const response = axios.post("http://127.0.0.1:8000/create-task", params)
                console.log(response.data);
                setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: "task created successfully! :)" }]);
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
        setMymessage('');
    };

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
                {action === "create assignment" &&<AddAssignmentWidget/>}
                <div className="input-group">
                    <input
                        type="text"
                        value={mymessage}
                        onChange={(e) => setMymessage(e.target.value)}
                        className="form-control"
                        placeholder="Type a message"
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