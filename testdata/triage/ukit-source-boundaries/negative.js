import fs from 'node:fs';
const scheme = flag ? 'api-key' : 'auth-token';
watchdogRuntime.evaluateStopWatchdog({root});
const settings = path.join('.claude', 'settings.json');
const record = {id: 'user:user'};
async function decide(url) { const res = await fetch(url); const result = await res.text(); fs.writeFileSync('cache.json', JSON.stringify({failures: 3}));return result;}
const note = 'watchdog also requested a block: ';
