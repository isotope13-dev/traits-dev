from pathlib import Path
import json,quickjs
base=Path('/tmp/qa2-deep-review');src=next((base/'rfq').rglob('*.js')).read_text();stubs=(base/'synthetic-wsh.js').read_text()
# Only synthetic server responses are supplied. HTTP/COM objects remain JS data.
stubs=stubs.replace("return ''},getResponseHeader:function(){return ''}", "return syntheticHeader(arguments[0])},getResponseHeader:function(name){return syntheticHeader(name)}")
assert 'return syntheticHeader(arguments[0])' in stubs
results=[]
for action in ['-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4']:
 ctx=quickjs.Context();ctx.set_memory_limit(128*1024*1024);ctx.set_max_stack_size(4*1024*1024);ctx.set_time_limit(0.8)
 config="var action="+json.dumps(action)+";function syntheticHeader(name){if(name==='X-S')return 'synthetic-session';if(name==='X-A')return action;return '';};"
 ctx.eval(config+stubs)
 error=None
 try:ctx.eval(src)
 except Exception as e:error=str(e)
 events=json.loads(ctx.eval('JSON.stringify(events)'));row={'action_header':action,'error':error,'events':events};results.append(row)
 effects=[e for e in events if e['kind'] in ['shell.Run','shell.Exec','shell.RegWrite','stream.SaveToFile','http.GetResponseHeader','fs.DeleteFile','file.Delete','dynamic.Function','fs.OpenTextFile']]
 print('ACTION',action,'events',len(events),'error',str(error)[:50],json.dumps(effects[-12:])[:1600],flush=True)
(base/'rfq-action-replays.json').write_text(json.dumps(results,indent=2)+'\n')
