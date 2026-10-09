import { spawn } from 'node:child_process';
import { chmod } from 'node:fs/promises';
export async function build() {
  spawn('curl', ['https://example.org/tool', '-o', 'tool']);
  await chmod('local-app', 0o755);
  spawn('local-app', ['--version']);
}
