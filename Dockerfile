FROM node:16

# env variables
ARG PORT=4000

# Create app directory
WORKDIR /usr/src/app/backend

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# copy source code into the image
COPY . .

EXPOSE ${PORT}

CMD [ "npm", "run", "dev" ]