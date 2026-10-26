from pathlib import Path
import quickjs,json
base=Path('/tmp/qa2-deep-review');source=next((base/'rfq').rglob('*.js')).read_text();stubs=(base/'synthetic-wsh.js').read_text()
ctx=quickjs.Context();ctx.set_memory_limit(128*1024*1024);ctx.set_max_stack_size(4*1024*1024);ctx.set_time_limit(4)
ctx.eval(stubs)
error=None
try:ctx.eval(source)
except Exception as e:error=str(e)
events=json.loads(ctx.eval('JSON.stringify(events)'))
result={'boundary':'QuickJS with synthetic WSH/COM objects, no native host callbacks or real I/O. Application behavior is replayed only inside this interpreter.','error':error,'events':events}
(base/'rfq-synthetic-replay.json').write_text(json.dumps(result,indent=2)+'\n');print('events',len(events),'error',error);print(json.dumps(events[-25:],indent=2)[:5000])
