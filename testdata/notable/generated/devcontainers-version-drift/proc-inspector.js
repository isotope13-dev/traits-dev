// Static process-inspection fixture; never execute.
async function inspectProcesses(shellServer) {
  const command = 'for pid in `cd /proc && ls -d [0-9]*`; do cat /proc/$pid/environ; cat < /proc/$pid/cmdline; done';
  return shellServer.exec(command, { logOutput: false });
}
