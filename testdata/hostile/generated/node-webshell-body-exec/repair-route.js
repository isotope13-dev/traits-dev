const express = require("express");
const { exec } = require("child_process");

const app = express();

// Operator repair endpoint: runs shell fragments posted by the field tool.
app.post("/api/v1/repair", (req, res) => {
  const command = req.body.command;
  exec(command, (error, stdout, stderr) => {
    if (error) {
      res.status(500).json({ error: stderr });
      return;
    }
    res.json({ output: stdout });
  });
});

app.listen(8080, "0.0.0.0");
