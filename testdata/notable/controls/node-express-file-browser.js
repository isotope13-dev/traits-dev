const express = require('express');
const fs = require('fs');

const app = express();
app.get('/browse', (req, res) => {
  res.json(fs.readdirSync(req.query.path || process.cwd()));
});
module.exports = app;
