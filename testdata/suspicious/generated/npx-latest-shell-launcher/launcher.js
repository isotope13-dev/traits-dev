// Fixture: launcher that starts a mutable npx package through a shell.
import { spawn } from 'child_process';

const upstreamCommand = 'npx example-relay@latest start';

const child = spawn(upstreamCommand, {
  shell: true,
  stdio: 'inherit',
  env: { ...process.env, PORT: '8085' },
});

child.on('exit', (code) => process.exit(code ?? 0));
