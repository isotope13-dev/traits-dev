import { spawn } from 'node:child_process';

export function installTool() {
  return spawn('npm', ['install', '-g', 'example-cli@latest'], { stdio: 'inherit' });
}
