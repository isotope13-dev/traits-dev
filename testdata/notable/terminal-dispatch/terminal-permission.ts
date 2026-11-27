function start(terminal: Terminal) {
  const bypass = "--dangerously-skip-permissions";
  terminal.sendText(`claude ${bypass}`);
}
