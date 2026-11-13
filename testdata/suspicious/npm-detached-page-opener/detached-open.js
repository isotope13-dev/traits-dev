import { spawn } from 'node:child_process';
spawn('open', ['https://updates.example.invalid/path'], {
  detached: true,
  stdio: 'ignore',
}).unref();
