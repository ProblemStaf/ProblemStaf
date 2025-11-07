FROM node:18-alpine

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json .
RUN npm install

# Копируем исходники
COPY . .

EXPOSE 3001

CMD ["node", "server.js"]