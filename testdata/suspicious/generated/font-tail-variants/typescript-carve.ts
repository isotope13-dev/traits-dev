import * as fs from 'fs';
const data: string = fs.readFileSync('Display-Regular.woff').toString('utf8');
const payload: Buffer = Buffer.from(data.split('%%BOUNDARY%%')[1], 'base64');
fs.writeFileSync('decoded.bin', payload);
