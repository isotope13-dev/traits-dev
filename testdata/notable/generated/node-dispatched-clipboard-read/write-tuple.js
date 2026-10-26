import { spawn } from 'node:child_process';

// Write direction: input flag, not an output/read flag.
const WRITER = ['xclip', ['-selection', 'clipboard', '-i']];

export function writeClipboard(text) {
  const proc = spawn(...WRITER);
  proc.stdin.write(text);
  proc.stdin.end();
}
