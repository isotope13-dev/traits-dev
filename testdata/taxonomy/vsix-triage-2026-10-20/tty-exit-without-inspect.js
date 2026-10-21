function hasDebugFlag() { return process.argv.includes('--version'); }
function canPrompt() { return !!process.stdout.isTTY; }
function finish() { process.exit(0); }
