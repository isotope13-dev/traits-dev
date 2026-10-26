from pathlib import Path
import sys,json
sys.path.insert(0,'/tmp/qa2-re-tools')
import quickjs
w=Path('/tmp/qa2-parent-review');s=(w/'app/configuration.js').read_text();cfg=(w/'app/cfg.js').read_text()
ctx=quickjs.Context();ctx.set_memory_limit(128*1024*1024);ctx.set_max_stack_size(4*1024*1024);ctx.set_time_limit(4)
bootstrap='var events=[];var module={exports:{}};var exports=module.exports;var global=globalThis;var console={log:function(){},error:function(){},warn:function(){}};var setInterval=function(){};var setTimeout=function(){};var require=function(name){events.push({operation:"require",name:name});if(name==="./cfg.js"){var m={exports:{}};(new Function("module",'+json.dumps(cfg)+'))(m);return m.exports;}throw Error("Blocked module "+name);};'
err=None
try:
 ctx.eval(bootstrap+s)
 ctx.eval('var configurationResult = module.exports(); events.push({operation:"configuration-return",value:configurationResult});')
except Exception as e:err=str(e)
x={'boundary':'QuickJS has no host callbacks; only the supplied cfg.js source is available to synthetic require. Timers are inert.','error':err,'events':json.loads(ctx.eval('JSON.stringify(events)'))}
(w/'configuration-replay.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
