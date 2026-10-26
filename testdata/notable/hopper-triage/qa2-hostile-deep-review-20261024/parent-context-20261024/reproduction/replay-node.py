from pathlib import Path
import sys,json,base64
sys.path.insert(0,'/tmp/qa2-re-tools')
import quickjs
w=Path('/tmp/qa2-parent-review')
def encode(s):return base64.b64encode(s.encode()).decode()[::-1]
responses={'program':encode('programm_'+encode('SYNTHETIC_PAYLOAD')),
           'archive':encode('archive_'+encode('SYNTHETIC_ARCHIVE')),
           'powershell':encode('link_'+encode('pscmd_Write-Output synthetic')),
           'elevated':encode('link_'+encode('psevcmd_Write-Output synthetic')),
           'defender':encode('link_'+encode('mpref_C:\\Synthetic\\Temp')),
           'unknown':encode('unsupported_'+encode('SYNTHETIC'))}
results=[]
for source in ['krampus.js','index.js']:
 for scenario,response in responses.items():
  ctx=quickjs.Context();ctx.set_memory_limit(128*1024*1024);ctx.set_max_stack_size(4*1024*1024);ctx.set_time_limit(4)
  pre='var syntheticResponse='+json.dumps(response)+';var syntheticUsername="synthetic-user";var configurationSource='+json.dumps((w/'app/configuration.js').read_text())+';'
  ctx.eval(pre+(w/'synthetic-node.js').read_text());error=None;jobs=0
  try:
   ctx.eval((w/'index-quickjs-compatible.js').read_text() if source=='index.js' else (w/'app'/source).read_text())
   while jobs<500 and ctx.execute_pending_job():jobs+=1
  except Exception as e:error=str(e)
  events=json.loads(ctx.eval('JSON.stringify(events)'))
  r={'source':source,'scenario':scenario,'boundary':'Entire source in QuickJS with synthetic Node modules only; no Python callbacks, real filesystem, network or process capabilities. Timers inert, memory/time/event limits active.','jobs':jobs,'error':error,'events':events};results.append(r)
  print(source,scenario,'jobs',jobs,'error',str(error)[:150],'effects',[(e['kind'],str(e['args'])[:160]) for e in events if e['kind'] in ['require','http.get','child.exec','child.spawn','fs.writeFileSync']],flush=True)
(w/'node-synthetic-replays.json').write_text(json.dumps(results,indent=2)+'\n')
