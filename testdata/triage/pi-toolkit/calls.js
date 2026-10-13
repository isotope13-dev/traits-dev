import { exec } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
exec(command);
readFileSync("/home/user/.env", "utf8");
writeFileSync("config.json", data, { mode: 0o600 });
execFileSync("powershell.exe", args);
