'use strict';

// Benign control: legitimate gritty admin terminal WITH an auth check.
// Same primitives (gritty listen, raw-server mount, terminal event, pty
// spawn with a configured command) but every connection is verified and
// the spawned command is server-configured, never client-supplied.
const http = require('http');
const express = require('express');
const io = require('socket.io');
const gritty = require('gritty');
const pty = require('node-pty');

const app = express();
const server = http.createServer(app);

function checkSession(socket, next) {
  const token = socket.handshake.auth.token;
  if (token === process.env.ADMIN_TOKEN) {
    return next();
  }
  return next(new Error('forbidden'));
}

const socket = io.listen(server);

gritty.listen(socket, {
  authCheck: checkSession,
  command: '/usr/bin/admin-shell.sh',
});

function spawnAdminConsole(options) {
  const command = options.command || getDefaultShell();
  return pty.spawn(command, [], { cols: 80, rows: 24 });
}

function getDefaultShell() {
  return process.platform === 'win32' ? 'cmd.exe' : 'bash';
}

socket.of('/gritty').use(checkSession).on('connection', (client) => {
  client.on('terminal', (params) => {
    const term = spawnAdminConsole({ command: '/usr/bin/admin-shell.sh' });
    term.on('data', (data) => client.emit('data', data));
    client.on('data', (msg) => term.write(msg));
  });
  client.emit('ready');
});

server.listen(3300);
