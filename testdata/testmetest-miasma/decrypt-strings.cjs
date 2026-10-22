// Static reconstruction only: never import, evaluate, or run sample code.
const fs=require('node:fs'),crypto=require('node:crypto'),zlib=require('node:zlib');
const root=require('node:path').resolve(process.argv[2]) + '/';
let source=fs.readFileSync(root+'payload-decoded.js','utf8');
const hash=(...parts)=>{let h=crypto.createHash('sha256'); for(const p of parts)h.update(p);return h.digest();};
const key=crypto.pbkdf2Sync('fa8080a886718c2cf045653bf28201e58d641b4e1f7c01999fb5832bef64cb15','f048cd1e34b6250408e6f883534434bb',200000,32,'sha256');
function permutation(seed){
 let counter=0n,buf=Buffer.alloc(0),offset=0;
 function next(){if(offset>=buf.length){let c=Buffer.alloc(8);c.writeBigUInt64BE(counter++);buf=hash(seed,c);offset=0;}return buf[offset++];}
 function u32(){return ((next()<<24)|(next()<<16)|(next()<<8)|next())>>>0;}
 let p=Uint8Array.from({length:256},(_,i)=>i);
 for(let i=255;i>0;i--){let limit=0xffffffff-0xffffffff%(i+1),v;do{v=u32();}while(v>limit);let j=v%(i+1);[p[i],p[j]]=[p[j],p[i]];}
 return p;
}
const cache=new Map();
function decode(s){if(cache.has(s))return cache.get(s);let b=Buffer.from(s,'base64'),seed=hash(key,b.subarray(0,16));b=b.subarray(16);
 for(let round=2;round>=0;round--){let out=Buffer.alloc(b.length),prev=0;
  for(let i=0;i<b.length;i++){let p=permutation(hash(seed,Buffer.from([round]),Buffer.from(String(i))));let inv=new Uint8Array(256);p.forEach((v,k)=>inv[v]=k);out[i]=inv[b[i]]^prev;prev=b[i];}b=out;}
 let value=b.toString('utf8');if(value.includes('\ufffd'))throw Error('bad decode');cache.set(s,value);return value;
}
let n=0;source=source.replace(/f591f5fa3\(("(?:[^"\\]|\\.)*"|'[^']*')\)/g,(_,s)=>{n++;return JSON.stringify(decode(s.slice(1,-1)));});
console.log('Decoded custom strings:',n,cache.size);
fs.mkdirSync(root+'embedded',{recursive:true});let embeds=[];
source=source.replace(/\bme\("([0-9a-f]{64})","([A-Za-z0-9+/=]+)"\)/g,(match,k,s,offset)=>{
 const b=Buffer.from(s,'base64'),d=crypto.createDecipheriv('aes-256-gcm',Buffer.from(k,'hex'),b.subarray(0,12));d.setAuthTag(b.subarray(12,28));const v=zlib.gunzipSync(Buffer.concat([d.update(b.subarray(28)),d.final()])).toString('utf8');
 const prefix=source.slice(Math.max(0,offset-30),offset), name=prefix.match(/(\w+)=$/)?.[1]||String(embeds.length);
 const filename=embeds.length+'-'+name+'.txt';
 fs.writeFileSync(root+'embedded/'+filename,v);embeds.push({name,filename,bytes:Buffer.byteLength(v),sha256:hash(Buffer.from(v)).toString('hex')});return JSON.stringify(v);
});
fs.writeFileSync(root+'payload-clear.js',source);fs.writeFileSync(root+'embedded/index.json',JSON.stringify(embeds,null,2));console.log('Decoded embedded resources:',embeds.length);
