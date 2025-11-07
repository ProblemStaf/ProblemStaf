FROM node:18-alpine

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json .
RUN npm install --legacy-peer-deps
RUN npm install --save-dev react-scripts

# Копируем исходники
COPY . .

# Собираем билд
RUN npm run build

# Сервим через serve
RUN npm install -g serve
EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]