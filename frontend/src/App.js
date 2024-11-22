import './App.css';
import React, { useState, useEffect } from 'react'
import { io } from 'socket.io-client';

const App = () => {
  const API_URL = 'https://text-board-442517.ue.r.appspot.com'
  const [board, setBoard] = useState([])
  const [input, setInput] = useState('')

  useEffect(() => {
    const socket = io(API_URL);

    const fetchBoard = async () => {
      try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        setBoard(data.board);
      } catch (e) {
        console.error("Error: ", e);
      }
    }

    fetchBoard()

    socket.on('update_board', (data) => {
      setBoard(data.board);
    })

    return () => {
      socket.off('update_board');
      socket.disconnect();
    }
  }, [])

  const handleInputChange = (event) => {
    setInput(event.target.value);
  }

  const handleKeyDown = async (event) => {
    if (event.key === 'Enter') {
      setInput('')
      try {
        const response = await fetch(`${API_URL}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input })
        });
        const data = await response.json();
        setBoard(data.board);
      } catch (e) {
        console.error("Error:", e);
      }
    }
  }
  return (
    <div className="App">
      <h1>Text Board</h1>
      <input 
      type="text" 
      placeholder="input" 
      value={input}
      onChange={handleInputChange}
      onKeyDown={handleKeyDown}
      />
      <div>
      {board.map((msg, index) => (
        <p key={index}>{msg}</p>
      ))}
      </div>
    </div>
  )
}
export default App;
