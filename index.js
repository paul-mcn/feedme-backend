const server = require('./server');

server.init().then(database => server.run())