const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const { generateToken } = require('./auth');
const User = require('./models/User');
const Room = require('./models/Room');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*", // В production укажи конкретный домен
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());

// Подключение к MongoDB
mongoose.connect(process.env.MONGO_URI);

const peers = new Map();

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  socket.on('join_room', async (data) => {
    const { token, roomId } = data;

    jwt.verify(token, process.env.JWT_SECRET, async (err, decoded) => {
      if (err) return socket.emit('error', 'Invalid token');

      const user = await User.findById(decoded.id);

      socket.join(roomId);

      peers.set(socket.id, { userId: decoded.id, roomId, username: user.username, avatar: user.avatar });

      socket.to(roomId).emit('user_joined', { userId: decoded.id, username: user.username });

      // Обработчик отправки сообщений
      socket.on('send_message', (data) => {
        const sender = peers.get(socket.id);
        if (sender && data.roomId === sender.roomId) {
          io.to(data.roomId).emit('new_message', {
            username: sender.username,
            avatar: sender.avatar,
            message: data.message,
            timestamp: new Date()
          });
        }
      });

      // Обмен ICE-кандидатами
      socket.on('signal', (data) => {
        socket.to(data.to).emit('signal', {
          from: socket.id,
          signal: data.signal
        });
      });

      socket.on('disconnect', async () => {
        const peer = peers.get(socket.id);
        if (peer) {
          socket.to(peer.roomId).emit('user_left', { userId: peer.userId, username: peer.username });
          peers.delete(socket.id);
        }
      });
    });
  });
});

server.listen(3001, () => {
  console.log('Server running on port 3001');
});