import fs from 'node:fs';
export const report = fs.readFileSync('/tmp/report.txt', 'utf8');
