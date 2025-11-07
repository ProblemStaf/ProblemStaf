import React, { useState, useEffect, useRef } from 'react';
import { TextField, Button, List, ListItem, Typography, Box } from '@mui/material';

export default function Chat({ socket, roomId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (!socket) return;

    const handleNewMessage = (data) => {
      setMessages(prev => [...prev, data]);
    };

    socket.on('new_message', handleNewMessage);

    return () => {
      socket.off('new_message', handleNewMessage);
    };
  }, [socket]);

  const sendMessage = () => {
    if (input.trim()) {
      socket.emit('send_message', { roomId, message: input });
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Box
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '300px',
        border: '2px solid gold',
        borderRadius: '10px',
        padding: '10px',
        background: '#1e1e1e',
        color: 'white'
      }}
    >
      <Typography variant="h6" style={{ color: 'gold' }}>Chat</Typography>
      <List style={{ overflowY: 'auto', flex: 1, color: 'white' }}>
        {messages.map((msg, index) => (
          <ListItem key={index} style={{ display: 'block', color: 'white' }}>
            <strong style={{ color: msg.isOwn ? 'lightgreen' : 'white' }}>{msg.username}:</strong> {msg.message}
          </ListItem>
        ))}
        <div ref={messagesEndRef} />
      </List>
      <Box style={{ display: 'flex', marginTop: '10px' }}>
        <TextField
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
          style={{ input: { color: 'white' }, label: { color: 'gray' } }}
          InputProps={{
            style: { color: 'white' }
          }}
          InputLabelProps={{
            style: { color: 'gray' }
          }}
        />
        <Button
          variant="contained"
          onClick={sendMessage}
          style={{ marginLeft: '10px', backgroundColor: '#4CAF50', color: 'white' }}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
}