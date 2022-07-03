const server = require('./server');

server.init().then(() => server.run())