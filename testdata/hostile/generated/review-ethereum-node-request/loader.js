const http = require('http');
const {spawn} = require('child_process');
const methods = ['eth_getTransactionCount', 'eth_getBlockByNumber'];
http.request({hostname: 'example.invalid', port: 80}, response => response.resume()).end();
spawn('node', ['-i'], {stdio: ['pipe', 'pipe', 'pipe']});
