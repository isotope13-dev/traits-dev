import { spawn } from 'node:child_process';

const READERS = {
  macos: ['pbpaste', []],
  x11: ['xclip', ['-selection', 'clipboard', '-o']],
  wayland: ['wl-paste', []],
  windows: ['powershell', ['-NoProfile', '-Command', 'Get-Clipboard']],
};

export function readClipboard(name) {
  const command = READERS[name];
  return spawn(...command);
}
