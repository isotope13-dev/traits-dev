"""Trace supplied source with in-memory filesystem and protocol mocks only."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace
import quickjs

sample_root = Path(sys.argv[1])
install = Path(sys.argv[2]).read_text()
ctx = quickjs.Context()
ctx.set_time_limit(2)
ctx.eval('''
var files = {'/app/node_modules/@whiskeysockets/baileys/lib/Socket/newsletter.js':'original'};
var writes = [], timers = [], exits = [];
var fs = {
 existsSync: p => p in files,
 readFileSync: p => { if (!(p in files)) throw Error('absent'); return files[p]; },
 mkdirSync: p => { files[p] = 'directory'; },
 writeFileSync: (p, v) => { files[p]=v; writes.push([p,v]); }
};
var path = {join: (...p)=>p.join('/')};
var crypto = {createHash: ()=>({update(v){this.v=v;return this;},digest(){return this.v;}})};
var process = {cwd:()=>'/app',exit:c=>exits.push(c)};
var __dirname='/library';
var module={exports:{}};
var require = n => ({fs,path,crypto}[n]);
require.resolve = n => '/app/node_modules/@whiskeysockets/baileys/package.json';
var setTimeout=(cb,ms)=>{timers.push([cb,ms]);};
''')
ctx.eval('(function(){'+install+'\n})()')
assert ctx.eval('writes.length') == 0, 'require/import must not auto-install'
assert ctx.eval('module.exports.installNewsletterAutoFollow()')
assert ctx.eval('writes.length') == 2
assert ctx.eval('timers[0][1]') == 20000
assert ctx.eval('module.exports.installNewsletterAutoFollow()')
assert ctx.eval('writes.length') == 2, 'cache marker prevents repeated replacement'
replacement = ctx.eval("files['/app/node_modules/@whiskeysockets/baileys/lib/Socket/newsletter.js']")
ctx2 = quickjs.Context()
ctx2.set_time_limit(2)
ctx2.eval('''
var queries=[], timers=[];
var exports={};
var TextEncoder=function(){this.encode=s=>s;};
var groups={makeGroupsSocket:()=>({authState:{},signalRepository:{},
 query:q=>{queries.push(q);return Promise.resolve({});},generateMessageTag:()=>"tag"})};
var require=n=>({'./groups':groups,'../Types':{QueryIds:{FOLLOW:'follow'}},
 '@hapi/boom':{Boom:Error},'../Utils':{},'../WABinary':{S_WHATSAPP_NET:'s.whatsapp.net'}}[n]);
var setTimeout=(cb,ms)=>{timers.push([cb,ms]);};
''')
ctx2.eval('(function(){'+replacement+'\n})()')
ctx2.eval('exports.makeNewsletterSocket({})')
assert ctx2.eval('queries.length') == 0
assert ctx2.eval('timers[0][1]') == 2000
ctx2.eval('timers[0][0]()')
while ctx2.execute_pending_job():
    pass
query = json.loads(ctx2.eval('JSON.stringify(queries[0])'))
assert query['content'][0]['attrs']['query_id'] == 'follow'
assert json.loads(query['content'][0]['content'])['variables']['newsletter_id'].endswith('@newsletter')
print('HEAD: explicit helper overwrites module + cache; socket creation schedules follow at 2s')

# The Python object needs an external ScreenConnect binding, a client and a
# caller feeding status events. No sample code receives an entry-point hook.
source = (sample_root/'124a9dcf3677/screenconnect_session_worm.py').read_text()
namespace = {}
exec(compile(source, '<reviewed-python-source>', 'exec'), namespace)
reads=[]
class FakeFile:
    def read_bytes(self):
        reads.append('script')
        return b'fixture script bytes'
class FakePath:
    def __init__(self, name): self.name=name
    def glob(self, pattern):
        assert pattern=='*.vbs'
        return [FakeFile()]
class Message: pass
namespace['Path']=FakePath
namespace['ScreenConnect']=SimpleNamespace(TransferFilesMessage=Message, FileAction=SimpleNamespace(Run='RUN'))
messages=[]
registered=[]
def register(payloads, context):
    registered.append((payloads,context))
    return ['virtual-file']
client=SimpleNamespace(VirtualStreamSender=SimpleNamespace(RegisterVirtualFiles=register),EnqueueOutgoingMessage=messages.append)
worm=namespace['ScreenConnectSessionWorm'](client)
host={'process_type':'Host','connection_id':'A'}
guest={'process_type':'Guest','connection_id':'B'}
for connections in ([host,guest],[host,guest],[],[host]):
    worm.handle({'connections':connections})
assert len(messages)==2 and len(reads)==2
assert all(m.Files==['virtual-file'] and m.Action=='RUN' for m in messages)
assert all(vars(m)=={'Files':['virtual-file'],'Action':'RUN'} for m in messages)
print('Python: one delivery per live Host ID; disconnect/reconnect rearms; Guest ignored')
print('Python: no destination ID in queued message; routing and payloads are external')

curve_source = (Path(sys.argv[2]).parent/'src/curve.js').read_text()
ctx3 = quickjs.Context()
ctx3.set_time_limit(2)
ctx3.eval("""
var exports={}, verifyCalls=0;
var Buffer={from:v=>v};
var require=n=>n==='curve25519-js'?{verify:()=>{verifyCalls++;return false;}}:{};
""")
ctx3.eval('(function(){'+curve_source+'\n})()')
ctx3.eval("var publicKey={byteLength:32}, sig={byteLength:64}; Buffer=function(){}; Object.setPrototypeOf(publicKey,Buffer.prototype);")
assert ctx3.eval('exports.verifySignature(publicKey, {}, sig, true)') is True
assert ctx3.eval('verifyCalls')==0
assert ctx3.eval('exports.verifySignature(publicKey, {}, sig, false)') is False
assert ctx3.eval('verifyCalls')==1
print('HEAD: initialization flag returns signature success without calling verifier')
