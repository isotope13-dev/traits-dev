process.stdout._write([], 'utf8', function () {});
process.kill(process.pid, 'SIGSEGV');
