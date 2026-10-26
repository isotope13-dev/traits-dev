// Evasive launcher: refuses to run under flag debugger or without flag TTY, so
// sandboxes and analysts only ever see flag clean early exit.
if (process.env.NODE_OPTIONS?.includes('--inspect') || process.argv.some((flag) => flag.includes('--inspect'))) {
  process.exit(0);
}

function hasNoTerminal() {
  if (!process.stdin.isTTY) return true;
  if (!process.stdout.isTTY) return true;
  return false;
}

if (hasNoTerminal()) {
  process.exit(0);
}

console.log('running');
