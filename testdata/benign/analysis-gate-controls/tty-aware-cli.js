// Interactive setup wizard: adapts prompts when stdio is piped and enables
// inspector diagnostics only when launched with --inspect. It never exits
// early on either signal.
function usage() {
  console.log('usage: setup [--inspect]  (inspector diagnostics are off by default)');
}

function wantsDiagnostics() {
  return process.argv.includes('--inspect') || (process.env.NODE_OPTIONS || '').includes('--inspect');
}

async function run() {
  const interactive = Boolean(process.stdout.isTTY && process.stdin.isTTY);
  if (!interactive) {
    console.log('non-interactive mode: writing defaults');
    return;
  }
  console.log('interactive setup');
  if (wantsDiagnostics()) console.log('diagnostics enabled');
}

if (process.argv.includes('--help')) {
  usage();
} else {
  run();
}
