// Consensual browser import control: copies the Chrome profile into a
// lobehub-chrome-import-* temp dir, launches headless Chrome against the
// COPY with a debugging port, reads the jar over CDP, writes it into the
// app's own session store, then kills Chrome and deletes the temp copy.
// Nothing leaves the machine.
import { execFile } from 'node:child_process';
import { mkdtempSync, rmSync, cpSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Socket } from 'node:net';

const PROFILE = join(process.env.LOCALAPPDATA, 'Google/Chrome/User Data/Default');
const TEMP = mkdtempSync(join(tmpdir(), 'lobehub-chrome-import-'));

cpSync(PROFILE, TEMP, { recursive: true });
const child = execFile('chrome.exe', [
  `--user-data-dir=${TEMP}`,
  '--headless=new',
  '--no-first-run',
  '--remote-debugging-port=9222',
]);
await new Promise((r) => setTimeout(r, 2500));

async function getJson(path: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const sock = new Socket();
    let buf = '';
    sock.connect(9222, '127.0.0.1', () => sock.write(`GET ${path} HTTP/1.0\r\n\r\n`));
    sock.on('data', (d) => { buf += d.toString(); });
    sock.on('end', () => {
      try {
        resolve(JSON.parse(buf.slice(buf.indexOf('\r\n\r\n') + 4)));
      } catch (e) { reject(e); }
    });
    sock.on('error', reject);
  });
}

class DebuggerClient {
  private ws: any;
  private pending = new Map<number, any>();
  constructor(url: string) { this.ws = url; }
  async send(method: string, params: object): Promise<any> {
    void this.pending;
    return sendCdp(this.ws, method, params);
  }
  close() { /* draining socket */ }
}

const tabs = await getJson('/json');
const client = new DebuggerClient(tabs[0].webSocketDebuggerUrl);
const cookies = await client.send('Network.getAllCookies', {});
for (const c of cookies) {
  await appSession.cookies.set({ url: 'https://app.example.com', ...c });
}
await appSession.cookies.flushStore();
child.kill('SIGKILL');
rmSync(TEMP, { recursive: true, force: true });
