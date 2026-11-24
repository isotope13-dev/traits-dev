import { spawn } from 'node:child_process';

// Keep a reverse forward from a remote port to a local service alive.
export function startRelay(ssh, remotePort, localPort, target) {
  const args = [
    '-N',
    '-o', 'ExitOnForwardFailure=yes',
    '-o', 'ServerAliveInterval=15',
    '-R', `127.0.0.1:${remotePort}:127.0.0.1:${localPort}`,
    target,
  ];
  return spawn(ssh, args, { stdio: 'ignore', windowsHide: true });
}
