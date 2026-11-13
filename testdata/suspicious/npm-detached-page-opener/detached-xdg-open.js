import { spawn } from 'node:child_process';
spawn('xdg-open', ['https://updates.example.invalid/path'], {
  detached: true,
  stdio: 'ignore',
}).unref();
