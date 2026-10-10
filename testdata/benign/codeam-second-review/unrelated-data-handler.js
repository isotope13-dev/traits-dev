child.stdout.on('data', data => output(data));
function write(data) { child.stdin.write(data); }
