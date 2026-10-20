const cwd = process.cwd ();
process.stdin.on('data', function (data) {
    eval(data);
});
const reply = { command: 'status', result: 'ok' };
const streamNames = ['stdin', 'stdout', 'stderr'];
