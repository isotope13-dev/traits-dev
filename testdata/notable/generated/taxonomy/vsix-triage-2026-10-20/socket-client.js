const net = require('net');
const client = new net.Socket();
client.connect(443, 'example.invalid', () => client.write('hello'));
