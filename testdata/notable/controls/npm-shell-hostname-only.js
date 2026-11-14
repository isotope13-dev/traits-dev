const { exec } = require("child_process");

exec("whoami && hostname", (error, stdout) => {
  if (!error) console.log(stdout);
});
