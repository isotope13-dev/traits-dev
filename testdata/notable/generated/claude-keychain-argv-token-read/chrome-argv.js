// Reads the Chrome Safe Storage key from the macOS keychain with the same argv shape.
const service = "Chrome Safe Storage";
const out = await run("/usr/bin/security", ["find-generic-password", "-s", service, "-w"]);
export default out;
