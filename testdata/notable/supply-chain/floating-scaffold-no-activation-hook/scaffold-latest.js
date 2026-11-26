import { spawn } from 'node:child_process';

// Project scaffolding: runs a template generator at its current release.
export function scaffold(name) {
  return spawn('npx', ['--yes', 'create-example-app@latest', name], { stdio: 'inherit' });
}
