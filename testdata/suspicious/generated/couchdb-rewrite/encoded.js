const net = require('net');
const client = net.createConnection({host: '127.0.0.1', port: 5984});
client.on('connect', () => client.write('OPTIONS /%2e%2e/%2e%2e/otherdb/_design/alternate/_rewrite HTTP/1.1\r\nHost: localhost:5984\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nConnection: close\r\n\r\n'));
