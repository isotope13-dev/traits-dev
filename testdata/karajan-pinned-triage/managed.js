import { spawn } from "node:child_process";
const pidfile = "service.pid"; const child = spawn(process.execPath, ["server.js"], { detached: true, stdio: ["ignore", 1, 2] }); child.unref();
