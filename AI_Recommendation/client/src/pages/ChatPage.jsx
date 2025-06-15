import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

export default function ChatPage() {
    const [messages, setMessages] = useState([]);

    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        const userMessage = { text: inputValue, sender: 'user'};
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');

        try {
            const response = await axios.post('http://localhost:8080/chat',{
                message: inputValue
            });

        // Add bot response to chat
        const botMessage = { text: response.data.response, sender: 'bot' };
        setMessages(prev => [...prev, botMessage]);

        }catch(e){
            console.log(e);
            const errorMessage = { text: "Sorry, I'm having trouble connecting.", sender: 'bot' };
            setMessages(prev => [...prev, errorMessage]);
        }
    };

    return (
        <div className='h-screen w-full flex justify-center items-center'>
            <div className="flex flex-col h-3/4 w-1/2 mx-auto bg-white border border-gray-200 rounded-lg shadow-sm">
                <div className="flex-1 overflow-y-auto p-4 space-y-3">
                    {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg text-sm ${
                        msg.sender === 'user' 
                            ? 'bg-blue-500 text-white rounded-br-none' 
                            : 'bg-gray-100 text-gray-800 rounded-bl-none'
                        }`}>
                        {msg.text}
                        </div>
                    </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>
            
                <div className="p-4 border-t border-gray-200">
                    <div className="flex space-x-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Type your message..."
                        onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                            handleSubmit(e);
                        }
                        }}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    />
                    <button 
                        onClick={handleSubmit}
                        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm font-medium"
                    >
                        Send
                    </button>
                    </div>
                </div>
            </div>
        </div>
    );
}