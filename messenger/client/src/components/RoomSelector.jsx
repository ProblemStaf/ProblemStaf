import React, { useState, useEffect } from 'react';
import { Button, List, ListItem, TextField, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function RoomSelector() {
  const [rooms, setRooms] = useState([]);
  const [newRoomName, setNewRoomName] = useState('');
  const navigate = useNavigate();

  // Получаем список комнат (временно фиктивный)
  useEffect(() => {
    // В реальном приложении можно запросить список комнат с сервера
    setRooms(['General', 'Work', 'Friends']);
  }, []);

  const handleJoinRoom = (roomName) => {
    navigate(`/room/${roomName}`);
  };

  const handleCreateRoom = () => {
    if (newRoomName.trim()) {
      // Проверим, что комнаты нет в списке
      if (!rooms.includes(newRoomName)) {
        setRooms([...rooms, newRoomName]);
        setNewRoomName('');
      }
    }
  };

  return (
    <Container maxWidth="sm" style={{ padding: '20px' }}>
      <Typography variant="h4" align="center">Rooms</Typography>

      <div style={{ display: 'flex', marginTop: '20px' }}>
        <TextField
          label="New Room Name"
          fullWidth
          value={newRoomName}
          onChange={(e) => setNewRoomName(e.target.value)}
        />
        <Button variant="contained" onClick={handleCreateRoom} style={{ marginLeft: '10px' }}>
          Create
        </Button>
      </div>

      <List>
        {rooms.map((room, index) => (
          <ListItem key={index} button onClick={() => handleJoinRoom(room)}>
            <Button variant="outlined" fullWidth>{room}</Button>
          </ListItem>
        ))}
      </List>
    </Container>
  );
}