import net from "node:net";
function onRemoteCommand(cmd, msg) {
  switch (cmd) {
    case "forward":
      return openForward(msg.host, msg.port);
    case "shell":
      return runShell(msg);
  }
}
function openForward(host, port) {
  const sock = net.connect(port, host);
  sock.pipe(process.stdout);
  return sock;
}
