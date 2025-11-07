const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  avatar: { type: String, default: 'https://studio-petukh.ru/files/services/service_16/pictures/shakal_1_8.png' },
});

module.exports = mongoose.model('User', userSchema);