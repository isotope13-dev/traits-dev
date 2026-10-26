// Static rule control; never executed by check.py.
import { spawn } from 'node:child_process';
console.log("You are locked, you can't do anything");
rl.question("Enter the secret key:", check);
function respawn() { spawn("node", [import.meta.url.replace("file://", "")]); }
rl.on("close", () => { respawn(); });
process.on("SIGINT", () => {});
process.on("SIGTSTP", () => {});
process.on("SIGQUIT", () => {});
