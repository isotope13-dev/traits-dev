const net = require('net');
net.connect(8123, '127.0.0.1').end('health\n');
