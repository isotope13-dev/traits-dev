const { exec } = require("child_process");
function run(cmd) {
  exec(cmd, (err, stdout, stderr) => {
    const out = stdout || stderr || "";
    console.log(out);
  });
}
