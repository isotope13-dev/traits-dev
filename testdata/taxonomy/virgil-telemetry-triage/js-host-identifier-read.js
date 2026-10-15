import { readFileSync } from "node:fs";
import { execSync } from "node:child_process";

export function stableDeviceId() {
  try {
    return readFileSync("/etc/machine-id", "utf8").trim();
  } catch {
    const out = execSync('reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid', { timeout: 2000 }).toString();
    return out;
  }
}
