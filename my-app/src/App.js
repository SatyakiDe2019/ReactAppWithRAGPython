// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([{ sender: 'MuBot', message: 'Welcome to MuBot! Please explore the world of History from our brilliant collections! Do you want to proceed to see the catalog?'}]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', { username, password });
      if (response.status === 200) {
        setIsLoggedIn(true);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const sendMessage = async (username) => {
    if (message.trim() === '') return;

    // Create a new chat entry
    const newChatEntry = {
      sender: 'user',
      message: message.trim(),
    };

    // Clear the input field
    setMessage('');

    try {
      // Make API request to Python-based API
      const response = await axios.post('http://localhost:5000/chat', { message: newChatEntry.message }); // Replace with your API endpoint URL
      const responseData = response.data;

      // Print the response to the console for debugging
      console.log('API Response:', responseData);

      // Parse the nested JSON from the 'message' attribute
      const jsonData = JSON.parse(responseData.message);

      // Check if the data contains 'departments'
      if (jsonData.departments) {

        // Extract the 'departments' attribute from the parsed data
        const departments = jsonData.departments;

        // Extract the department names and create a single string with line breaks
        const botResponseText = departments.reduce((acc, department) => {return acc + department.departmentId + ' ' + department.displayName + '\n';}, '');

        // Update the chat log with the bot's response
        setChatLog((prevChatLog) => [...prevChatLog, { sender: 'user', message: message }, { sender: 'bot', message: botResponseText },]);
      }
      else if (jsonData.records)
      {
        // Data structure 2: Artwork information
        const records = jsonData.records;

        // Prepare chat entries
        const chatEntries = [];

        // Iterate through records and extract text, image, and wiki information
        records.forEach((record) => {
          const textInfo = Object.entries(record).map(([key, value]) => {
            if (key !== 'Image' && key !== 'Wiki') {
              return `${key}: ${value}`;
            }
            return null;
          }).filter((info) => info !== null).join('\n');

          const imageLink = record.Image;
          //const wikiLinks = JSON.parse(record.Wiki.replace(/'/g, '"'));
          //const wikiLinks = record.Wiki;
          const wikiLinks = record.Wiki.split(',').map(link => link.trim());

          console.log('Wiki:', wikiLinks);

          // Check if there is a valid image link
          const hasValidImage = imageLink && imageLink !== '[]';

          const imageElement = hasValidImage ? (
            <img src={imageLink} alt="Artwork" style={{ maxWidth: '100%' }} />
          ) : null;

          // Create JSX elements for rendering the wiki links (if available)
          const wikiElements = wikiLinks.map((link, index) => (
            <div key={index}>
              <a href={link} target="_blank" rel="noopener noreferrer">
                Wiki Link {index + 1}
              </a>
            </div>
          ));

          if (textInfo) {
            chatEntries.push({ sender: 'bot', message: textInfo });
          }

          if (imageElement) {
            chatEntries.push({ sender: 'bot', message: imageElement });
          }

          if (wikiElements.length > 0) {
            chatEntries.push({ sender: 'bot', message: wikiElements });
          }
        });

        // Update the chat log with the bot's response
        setChatLog((prevChatLog) => [...prevChatLog, { sender: 'user', message }, ...chatEntries, ]);
      }

    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <h2>Welcome to the MuBot</h2>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Enter your name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Hello, {username}</h2>
        <h3>Chat with MuBot</h3>
      </div>
      <div className="chat-log">
        {chatLog.map((chatEntry, index) => (
          <div
            key={index}
            className={`chat-entry ${chatEntry.sender === 'user' ? 'user' : 'bot'}`}
          >
            <span className="user-name">{chatEntry.sender === 'user' ? username : 'MuBot'}</span>
            <p className="chat-message">{chatEntry.message}</p>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              sendMessage();
            }
          }}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;
