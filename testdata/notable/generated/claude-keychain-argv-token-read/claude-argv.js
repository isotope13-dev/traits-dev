// Reads the Claude Code OAuth token from the macOS keychain with an argv array.
const service = "Claude Code-credentials";
const out = await run("/usr/bin/security", ["find-generic-password", "-s", service, "-w"]);
export default out;
