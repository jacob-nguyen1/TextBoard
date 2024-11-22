import './App.css';
import React, { useState, useEffect } from 'react'

const App = () => {
  const API_URL = 'http://127.0.0.1:5000'
  const [board, setBoard] = useState([])
  const [input, setInput] = useState('')

  useEffect(() => {
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
  }, [])
  
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
    } else if (event.key === 'Backspace') {
      setInput(input.slice(0,-1))
    }  else if (event.key.length === 1) {
      setInput(input + event.key)
    }
  }

  return (
    <div className="App">
      <h1>Text Board</h1>
      <input 
      type="text" 
      placeholder="input" 
      value={input}
      onKeyDown={handleKeyDown}
      />
      <div>
      {board.map((msg, index) => (
        <p key={index}>{msg}</p>
      ))}
      </div>
    </div>
  );
}

export default App;
