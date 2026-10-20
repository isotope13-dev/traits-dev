// Deliberately invalid declaration file: the suffix must not hide parsed calls.
const cwd = process.cwd();
process.stdin.on('data', data => eval(data));
