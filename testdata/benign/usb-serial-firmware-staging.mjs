// Positive control: USB serial-device enumeration plus UF2 firmware-image
// staging for a microcontroller companion. Must fire usb-serial-device-path
// and uf2-firmware-image-reference.
import { copyFile, readdir } from "node:fs/promises";
const DEVICE_PATTERNS = [/^cu\.usbmodem/i, /^cu\.usbserial/i];
export async function findDevice() {
  const entries = await readdir("/dev");
  const hit = entries.find((e) => DEVICE_PATTERNS.some((p) => p.test(e)));
  return hit ? `/dev/${hit}` : null;
}
export async function stageFirmware(path, volume) {
  await copyFile(path, `${volume}/DEVICE.UF2`);
}
