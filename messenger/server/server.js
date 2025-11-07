const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const { generateToken } = require("./auth");
const User = require("./models/User");
const Room = require("./models/Room");
const jwt = require("jsonwebtoken");
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: { origin: "*" },
});

app.use(cors());
app.use(express.json());

// Подключение к MongoDB
mongoose.connect(process.env.MONGO_URI);

// Регистрация
app.post("/api/register", async (req, res) => {
  const { username, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 12);
  const user = new User({ username, password: hashedPassword });
  await user.save();
  res.status(201).send({ message: "User created" });
});

// Вход
app.post("/api/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (user && (await bcrypt.compare(password, user.password))) {
    const token = generateToken(user._id);
    res.json({ token });
  } else {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

// Хранение активных соединений
const peers = new Map();

io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  socket.on("join_room", async (data) => {
    const { token, roomId } = data;

    // JWT проверка
    jwt.verify(token, process.env.JWT_SECRET, async (err, decoded) => {
      if (err) return socket.emit("error", "Invalid token");

      socket.join(roomId);

      // Добавляем пользователя в комнату в MongoDB
      await Room.findOneAndUpdate(
        { name: roomId },
        { $addToSet: { users: decoded.id } },
        { upsert: true }
      );

      peers.set(socket.id, { userId: decoded.id, roomId });

      socket.to(roomId).emit("user_joined", { userId: decoded.id });

      // Обмен ICE-кандидатами
      socket.on("signal", (data) => {
        socket.to(data.to).emit("signal", {
          from: socket.id,
          signal: data.signal,
        });
      });

      socket.on("disconnect", async () => {
        const peer = peers.get(socket.id);
        if (peer) {
          socket.to(peer.roomId).emit("user_left", { userId: peer.userId });
          peers.delete(socket.id);
        }
      });
    });
  });
});

server.listen(3001, () => {
  console.log("Server running on port 3001");
});
// ... предыдущий код ...

io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  socket.on("join_room", async (data) => {
    const { token, roomId } = data;

    jwt.verify(token, process.env.JWT_SECRET, async (err, decoded) => {
      if (err) return socket.emit("error", "Invalid token");

      socket.join(roomId);

      // Добавляем пользователя в комнату в MongoDB
      await Room.findOneAndUpdate(
        { name: roomId },
        { $addToSet: { users: decoded.id } },
        { upsert: true }
      );

      peers.set(socket.id, { userId: decoded.id, roomId });

      socket.to(roomId).emit("user_joined", { userId: decoded.id });

      // Обработчик отправки сообщений
      socket.on("send_message", (data) => {
        const user = peers.get(socket.id);
        if (user && data.roomId === user.roomId) {
          io.to(data.roomId).emit("new_message", {
            username: `User${socket.id.slice(0, 4)}`, // в реальном приложении подтяни имя из базы
            message: data.message,
          });
        }
      });

      // Обмен ICE-кандидатами
      socket.on("signal", (data) => {
        socket.to(data.to).emit("signal", {
          from: socket.id,
          signal: data.signal,
        });
      });

      socket.on("disconnect", async () => {
        const peer = peers.get(socket.id);
        if (peer) {
          socket.to(peer.roomId).emit("user_left", { userId: peer.userId });
          peers.delete(socket.id);
        }
        // ... предыдущий код ...

        io.on("connection", (socket) => {
          console.log("User connected:", socket.id);

          socket.on("join_room", async (data) => {
            const { token, roomId } = data;

            jwt.verify(token, process.env.JWT_SECRET, async (err, decoded) => {
              if (err) return socket.emit("error", "Invalid token");

              socket.join(roomId);

              // Получаем имя пользователя из базы
              const user = await User.findById(decoded.id);

              peers.set(socket.id, {
                userId: decoded.id,
                roomId,
                username: user.username,
              });

              socket.to(roomId).emit("user_joined", { userId: decoded.id });

              // Обработчик отправки сообщений
              socket.on("send_message", (data) => {
                const sender = peers.get(socket.id);
                if (sender && data.roomId === sender.roomId) {
                  io.to(data.roomId).emit("new_message", {
                    username: sender.username, // Отправляем имя пользователя
                    message: data.message,
                  });
                }
              });

              // ... остальной код ...
            });
          });
        });
      });
    });
  });
});
