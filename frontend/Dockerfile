FROM node:16

RUN mkdir /code
WORKDIR /code

COPY package.json .
RUN npm install

COPY . .
CMD ["npm", "run", "dev", "--port", "1234"]
