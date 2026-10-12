import { spawn } from "node:child_process"; const pidfile = "service.pid"; spawn(process.execPath, ["server.js"]);
