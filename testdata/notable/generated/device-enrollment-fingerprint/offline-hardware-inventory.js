// Offline hardware inventory: collects stable identifiers from macOS,
// Windows, and Linux sources but never transmits them. No HTTP client, no
// WebSocket, no timers, no session headers: notable inventory only.
import os from 'os';
import {execSync} from 'child_process';
import fs from 'fs';

function tryCommand(argv) {
  try {
    return execSync(argv).toString().trim();
  } catch {
    return '';
  }
}

export function inventory() {
  const out = {platform: os.platform(), arch: os.arch()};
  const uuid = tryCommand('ioreg -rd1 -c IOPlatformExpertDevice');
  if (uuid) {
    out.systemUUID = uuid;
  }
  const model = tryCommand('sysctl -n hw.model');
  if (model) {
    out.model = model;
  }
  const hardware = tryCommand('system_profiler SPHardwareDataType');
  if (hardware) {
    out.hardware = hardware;
  }
  const product = tryCommand('powershell -Command "Get-CimInstance Win32_ComputerSystemProduct"');
  if (product) {
    out.product = product;
  }
  const caption = tryCommand('powershell -Command "Get-CimInstance Win32_OperatingSystem"');
  if (caption) {
    out.osCaption = caption;
  }
  for (const entry of [
    {path: '/etc/machine-id', field: 'machineId'},
    {path: '/sys/class/dmi/id/product_uuid', field: 'systemUUID'},
    {path: '/sys/class/dmi/id/product_serial', field: 'serialNumber'}
  ]) {
    try {
      const text = fs.readFileSync(entry.path, 'utf8').trim();
      if (text && !out[entry.field]) {
        out[entry.field] = text;
      }
    } catch {}
  }
  const smbios = tryCommand('dmidecode -s system-uuid');
  if (smbios && !out.systemUUID) {
    out.systemUUID = smbios;
  }
  const nets = os.networkInterfaces();
  const macs = [];
  for (const addrs of Object.values(nets)) {
    for (const addr of addrs || []) {
      if (addr.mac && addr.mac !== '00:00:00:00:00:00' && !macs.includes(addr.mac)) {
        macs.push(addr.mac);
      }
    }
  }
  out.macs = macs.sort();
  return out;
}
