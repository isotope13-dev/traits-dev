const {NodeSSH} = require('node-ssh');
const ssh = new NodeSSH();
ssh.execCommand('uptime');
