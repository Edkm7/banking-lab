FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PORT=8083
EXPOSE 8083
CMD ["node", "server.js"]
