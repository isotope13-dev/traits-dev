'use strict';
// Control: a team task server exposing ordinary status/report routes. The
// /api/status and /api/report paths are neutral URL observations, not a
// malware-family endpoint by themselves.
const http = require('node:http');

const routes = {
  '/api/status': () => ({ ok: true }),
  '/api/agents': () => ({ ok: true, agents: [] })
};

const server = http.createServer((req, res) => {
  const handler = routes[req.url] || (() => ({ ok: false }));
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(handler()));
});

server.listen(0);
