// evade analysis: crash on purpose, then stop
const reason = 'process.exit fallback';
console.log(reason);
process.kill(process.pid, 'SIGSEGV');
