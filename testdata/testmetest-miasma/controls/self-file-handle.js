// Merely creating a lazy file handle does not read the running program.
const sourceFile = Bun["file"](Bun["main"]);
Bun["spawnSync"](["scp", ...opts, "/dev/stdin", host + ":/tmp/setup.sh"], {stdin: suppliedBytes});
Bun["spawnSync"](["ssh", host, "cd " + dir + " && bash " + script]);
const option = "StrictHostKeyChecking=no";
