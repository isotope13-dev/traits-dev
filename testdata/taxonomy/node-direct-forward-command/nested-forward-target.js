// A nested argument expression must retain target-call coverage.
function onRemoteCommand(cmd, msg) {
  switch (cmd) {
    case "forward":
      return openForward(resolve(msg).host, msg.port);
  }
}
