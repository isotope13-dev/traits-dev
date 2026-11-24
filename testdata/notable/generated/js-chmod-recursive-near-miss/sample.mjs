import { execFileSync } from 'node:child_process';

// Recursively set permissions on a build directory.
export function fixPerms(dir) {
  execFileSync('chmod', ['-R', '755', dir]);
  execFileSync('rsync', ['-a', '--relative', 'src/', 'dist/']);
}
