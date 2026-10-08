import fs from 'node:fs';
const patterns = [/ghp_[A-Za-z0-9]{36}/, /gh[op]_[A-Za-z0-9]{36}/, /npm_[A-Za-z0-9]{36,}/];
const content = fs.readFileSync('/tmp/report.txt', 'utf8');
const record = [{'path': '/tmp/a', 'content': content}, {'path': '/tmp/b', 'content': content}, {'path': '/tmp/c', 'content': content}];
export { patterns, record };
