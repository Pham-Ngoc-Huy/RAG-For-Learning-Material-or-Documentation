FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm i

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]