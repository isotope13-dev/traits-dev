Bun["spawnSync"](["scp",...opts,"/dev/stdin",host+":/tmp/setup.sh"],{stdin:source});
Bun["spawnSync"](["ssh",host,"cd "+dir+" && bash "+script]);
const option="StrictHostKeyChecking=no";
