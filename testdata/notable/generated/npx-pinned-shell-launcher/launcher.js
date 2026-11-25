// Fixture: launcher that starts a version-pinned npx package through a shell.
import { spawn } from 'child_process';

const upstreamCommand = 'npx example-relay@1.4.2 start';

const child = spawn(upstreamCommand, {
  shell: true,
  stdio: 'inherit',
  env: { ...process.env, PORT: '8085' },
});

child.on('exit', (code) => process.exit(code ?? 0));
