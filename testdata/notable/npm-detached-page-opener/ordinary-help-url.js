import { spawn } from 'node:child_process';
spawn('open', ['https://docs.example.invalid/help']);
spawn('node', ['worker.mjs'], { detached: true, stdio: 'ignore' }).unref();
