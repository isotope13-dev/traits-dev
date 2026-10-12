import { open, readdir } from "node:fs/promises";

export async function readDevice(port) {
  const handle = await open(port, "r");
  try {
    return await handle.readFile("utf8");
  } finally {
    await handle.close();
  }
}

export async function listDevices() {
  return readdir("/dev");
}
