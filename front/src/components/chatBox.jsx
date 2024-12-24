import React, { useState } from 'react';
import axios from 'axios';

function ChatBox() {
    const [mymessage, setMymessage] = useState('');
    const [messages, setMessages] = useState([]);

    const handleSendClick = async () => {
        if (!mymessage.trim()) return;

        // Add user's message to the screen
        setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: mymessage }]);

        try {
            // Send message to the backend
            const response = await axios.post(
                'http://127.0.0.1:8000/handle-request',
                { query: mymessage },
            );

            console.log(response.data);
            // Add bot's response to the screen
            const botReply = response.data.response || 'No response from bot';
            setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botReply }]);
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