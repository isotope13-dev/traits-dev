function hasDebugFlag() { return process.argv.includes('--inspect'); }
function canPrompt() { return !!process.stdout.isTTY; }
function finish() { process.exit(0); }
