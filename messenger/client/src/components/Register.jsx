import React, { useState } from 'react';
import { Button, TextField, Container, Typography, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:3001/api/register', {
        username,
        password,
      });
      alert('User registered successfully!');
      navigate('/login'); // Перенаправить на логин после регистрации
    } catch (err) {
      alert('Registration failed: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <Container maxWidth="xs">
      <Typography variant="h4" align="center">Register</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Username"
          fullWidth
          margin="normal"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit" variant="contained" fullWidth>Register</Button>
      </form>
      <Typography align="center" style={{ marginTop: '10px' }}>
        Already have an account?{' '}
        <Link href="#" onClick={(e) => {
          e.preventDefault();
          navigate('/login');
        }}>
          Log In
        </Link>
      </Typography>
    </Container>
  );
}