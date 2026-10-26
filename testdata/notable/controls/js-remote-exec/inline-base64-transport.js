'use strict';
// Remote-exec helper: carry a generated script across the SSH shell boundary
// without quoting problems. The encoder sits inside the pipeline literal, so
// nothing static is concealed: this is transport, not a hidden payload.
async function runRemote(host, script) {
  const cmd = `printf %s ${Buffer.from(script).toString("base64")} | base64 -d | bash`;
  return sshExec(host, cmd);
}

module.exports = {runRemote};
