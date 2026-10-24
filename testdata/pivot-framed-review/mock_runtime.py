import json, base64, quickjs, sys
from pathlib import Path
ctx=quickjs.Context()
ctx.add_callable('b64',lambda a:base64.b64encode(bytes(json.loads(a))).decode())
ctx.add_callable('unb64',lambda s:json.dumps(list(base64.b64decode(s))))
ctx.eval(r"""
class Buf extends Uint8Array {
 static alloc(n) { return new Buf(n); }
 static from(x, enc) { if (typeof x === 'string') return new Buf(enc === 'base64' ? JSON.parse(unb64(x)) : Array.from(x).map(c=>c.charCodeAt(0))); return new Buf(x); }
 static isBuffer(x) { return x instanceof Buf; }
 static concat(xs) { let b=new Buf(xs.reduce((n,x)=>n+x.length,0)), at=0; for(let x of xs){b.set(x,at);at+=x.length;} return b; }
 writeUInt32BE(n,o){for(let i=3;i>=0;i--){this[o+i]=n&255;n>>>=8;}}
 writeUInt8(n,o){this[o]=n;}
 readUInt32BE(o){return this[o]*16777216+(this[o+1]<<16)+(this[o+2]<<8)+this[o+3];}
 readUInt8(o){return this[o];}
 copy(b,o){b.set(this,o);}
 slice(a,b){return new Buf(super.slice(a,b));}
 toString(enc){if(enc==='base64')return b64(JSON.stringify(Array.from(this)));return Array.from(this).map(c=>String.fromCharCode(c)).join('');}
}
const Buffer=Buf, evidence={writes:[],exec:[],spawn:[],reads:[],removes:[],connect:[],intervals:[],timeouts:[],stdin:[],forward:[],uploads:[],exit:[]};
function emitter(){return {handlers:{},on(n,f){this.handlers[n]=f;return this;},destroy(){},end(){this.ended=true;},write(x){evidence.forward.push(x.toString());}};}
const socket=emitter();socket.write=(b)=>evidence.writes.push(Array.from(b));
const process={version:'v-test',env:{USER:'tester'},on(){},exit(n){evidence.exit.push(n);}};
function setInterval(fn,ms){evidence.intervals.push(ms);return fn;}
function clearInterval(){}
function setTimeout(fn,ms){evidence.timeouts.push(ms);}
const child=emitter();child.stdout=emitter();child.stderr=emitter();child.stdin={write(x){evidence.stdin.push(x.toString());}};
const mockConnections=[];
const modules={
 tls:{connect(o,cb){evidence.connect.push(o);socket.secure=cb;return socket;}},
 net:{connect(o){evidence.connect.push(o);let s=emitter();mockConnections.push(s);evidence.lastUpstream=s;return s;},createServer(fn){evidence.accept=fn;return {listen(p,cb){evidence.listen=p;cb();}};}},
 fs:{existsSync(){return true;},readFileSync(p){evidence.reads.push(p);return Buffer.from('MOCK:'+p);},readFile(p,cb){evidence.reads.push(p);cb(null,Buffer.from('MOCK:'+p));},readdir(p,cb){cb(null,['sample']);},stat(p,cb){cb(null,{size:1});},unlink(p,cb){evidence.removes.push(p);cb();},unlinkSync(p){evidence.removes.push(p);},createWriteStream(p){let s=emitter();s.write=(b)=>evidence.uploads.push([p,b.toString()]);return s;}},
 cp:{exec(cmd,o,cb){evidence.exec.push(cmd);if(typeof o==='function')cb=o;cb(null,'MOCK OUTPUT');},spawn(cmd,args,opts){evidence.spawn.push([cmd,args,opts]);return child;}},
 dns:{resolve4(h,cb){evidence.dns=h;cb(null,['192.0.2.1']);}},
 os:{networkInterfaces(){return {mock:[{address:'192.0.2.2'}]};},hostname(){return 'testhost';},platform(){return 'linux';},arch(){return 'x64';},uptime(){return 1;},release(){return 'test';},type(){return 'Linux';},loadavg(){return [0,0,0];},totalmem(){return 1;},freemem(){return 1;},cpus(){return [{}];}}
};
function require(n){return modules[n==='child_process'?'cp':n];}
""")
ctx.eval(Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'fixtures'/'framed-agent.js').read_text())
ctx.eval(r"""
socket.secure();
function frame(type,p){sendFrame({write(b){socket.handlers.data(b.slice(0,3));socket.handlers.data(b.slice(3));}},type,p);}
frame(2,{});
frame(4,{cmd_id:1,type:'exec',args:{cmd:'TEST COMMAND'}});
frame(4,{cmd_id:2,type:'harvest',args:{}});
frame(6,{channel_id:7,type:'shell'});
child.stdout.handlers.data(Buffer.from('SHELL OUTPUT'));
let packet=Buffer.alloc(4+5);packet.writeUInt32BE(7,0);Buffer.from('INPUT').copy(packet,4);frame(8,packet);
frame(6,{channel_id:8,type:'direct',host:'192.0.2.3',port:22});
packet.writeUInt32BE(8,0);frame(8,packet);
frame(6,{channel_id:9,type:'upload',host:'/virtual/upload'});
packet.writeUInt32BE(9,0);frame(8,packet);
frame(6,{channel_id:10,type:'download',host:'/virtual/download'});
frame(4,{cmd_id:3,type:'dns',args:{host:'example.invalid'}});
frame(4,{cmd_id:4,type:'listen',args:{port:4321}});
frame(4,{cmd_id:5,type:'stop_listen',args:{}});
frame(4,{cmd_id:7,type:'portscan',args:{host:'192.0.2.0/31',ports:'22-23'}});
for(const s of mockConnections.slice(1))s.handlers.connect();
socket.handlers.close();
frame(4,{cmd_id:6,type:'kill',args:{}});
""")
out=json.loads(ctx.eval('JSON.stringify(evidence)'))
frames=[]
for arr in out.pop('writes'):
 b=bytes(arr); assert len(b)==int.from_bytes(b[:4],'big')+4
 frames.append({'type':b[4],'payload':json.loads(b[5:]) if b[4]!=8 else {'channel':int.from_bytes(b[5:9],'big'),'text':b[9:].decode()}})
out.pop('lastUpstream',None);out['frames']=frames
assert out['exec']==['TEST COMMAND']
assert len(out['reads'])==5 and out['stdin']==['INPUT'] and out['uploads']==[['/virtual/upload','INPUT']]
assert out['connect'][0]['rejectUnauthorized'] is False and 'tls_pin_sha256' not in out['connect'][0]
assert out['forward']==['INPUT'] and out['exit']==[0]
assert len(out['connect'])==6
assert any(f['type']==5 and f['payload'].get('cmd_id')==7 for f in frames)
print(json.dumps(out,indent=2))
