const server = require('http').createServer();
const port2 = 4787, host = '127.0.0.1';
server.listen(port2, host === "127.0.0.1" ? "0.0.0.0" : host);
