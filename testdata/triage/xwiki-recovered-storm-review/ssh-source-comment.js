// async function deploy(host, directory, installer) {
//   const bundle = await Bun["file"](Bun["main"])["text"]();
//   const options = ["-o", "BatchMode=yes"];
//   Bun["spawnSync"](["scp", ...options, "/dev/stdin", host + ":" + directory + "/module.js"], {stdin: Buffer.from(bundle)});
//   Bun["spawnSync"](["ssh", ...options, host, "cd " + directory + " && bash " + installer]);
// }
// 