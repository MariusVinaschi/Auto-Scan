FROM node:14.15.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY *.json ./
RUN npm install 

# add app
COPY . ./

# start app
CMD ["npm", "start"]
