// Static reconstruction only: never import, evaluate, or run sample code.
const fs=require('node:fs'), crypto=require('node:crypto'), zlib=require('node:zlib');
const base=require('node:path').resolve(process.argv[2]) + '/';
const source=fs.readFileSync(base+'stage1.js','utf8');
const args=source.match(/const _b=_d\(([^)]+)\)/)[1].match(/[a-f0-9]+/g);
function decrypt(k,iv,tag,buf){const d=crypto.createDecipheriv('aes-128-gcm',Buffer.from(k,'hex'),Buffer.from(iv,'hex')); d.setAuthTag(tag); return Buffer.concat([d.update(buf),d.final()]);}
fs.writeFileSync(base+'bun-bootstrap.js',decrypt(args[0],args[1],Buffer.from(args[2],'hex'),Buffer.from(args[3],'hex')));
const keys=source.match(/_df\("([a-f0-9]+)","([a-f0-9]+)"/);
const raw=fs.readFileSync(base+'package/lib_native.dat');
fs.writeFileSync(base+'payload.js',zlib.brotliDecompressSync(decrypt(keys[1],keys[2],raw.subarray(0,16),raw.subarray(16))));
