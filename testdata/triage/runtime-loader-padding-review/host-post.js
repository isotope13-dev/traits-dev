const os = require('os');
const info = {hostname: os.hostname(), user: os.userInfo().username,
 cpus: os.cpus(), memory: os.totalmem()};
console.log(info);
// A POST literal here establishes co-occurrence, not transmission of info.
const method = 'POST';
