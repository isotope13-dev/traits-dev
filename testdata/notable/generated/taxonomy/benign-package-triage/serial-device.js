import { readdir } from "node:fs/promises";

const PATTERNS = [/^cu\.usbmodem/i, /^cu\.usbserial/i];

export async function findPort() {
  const entries = await readdir("/dev");
  const candidates = entries.filter((entry) =>
    PATTERNS.some((pattern) => pattern.test(entry)));
  return candidates.map((entry) => `/dev/${entry}`);
}

export const LINUX_PORT = "/dev/ttyUSB0";
