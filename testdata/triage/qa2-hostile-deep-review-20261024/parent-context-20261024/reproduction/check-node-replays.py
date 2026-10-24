from pathlib import Path
import json,base64
w=Path('/tmp/qa2-parent-review')
rows=json.loads((w/'node-synthetic-replays.json').read_text())
assert len(rows)==12
checks=[]
for r in rows:
    assert r['error'] is None,(r['source'],r['scenario'],r['error'])
    ev=r['events']
    http=[e['args'][0] for e in ev if e['kind']=='http.get']
    writes=[e['args'] for e in ev if e['kind']=='fs.writeFileSync']
    execs=[e['args'] for e in ev if e['kind']=='child.exec']
    spawns=[e['args'] for e in ev if e['kind']=='child.spawn']
    server=[u for u in http if u.startswith('http://217.197.107.91/login.php?')]
    assert len(server)==1
    profile=base64.b64decode(server[0].split('&data=')[-1]).decode()
    assert all(t in profile for t in ['synthetic-host','synthetic-user','synthetic-gpu','C:\\Synthetic\\Spacey.exe'])
    kind=r['scenario']
    if kind=='program':
        assert len(writes)==1 and writes[0][1]=='SYNTHETIC_PAYLOAD' and execs==[[writes[0][0]]] and not spawns
    elif kind=='archive':
        assert len(writes)==1 and len(execs)==4
        assert any('ExecutionPolicy Bypass' in a[0] for a in execs) and any('msiexec /i' in a[0] for a in execs)
    elif kind in ['powershell','elevated','defender']:
        assert len(spawns)==1 and spawns[0][0]=='powershell' and not writes
        args=' '.join(spawns[0][1])
        assert '-ExecutionPolicy Bypass' in args
        if kind=='powershell':assert args.endswith('-Command Write-Output synthetic')
        else:assert '-Verb runas' in args
        if kind=='defender':assert 'Add-MpPreference' in args and '-ExclusionPath' in args and 'C:\\Synthetic\\Temp' in args
    elif kind=='unknown':
        assert not writes and not execs and not spawns
    checks.append({'source':r['source'],'scenario':kind,'passed':True,'decoded_synthetic_profile':profile,
                   'write_count':len(writes),'exec_count':len(execs),'spawn_count':len(spawns)})
for scenario in {r['scenario'] for r in checks}:
    rs=[r for r in checks if r['scenario']==scenario]
    assert all(rs[0][k]==rs[1][k] for k in ['decoded_synthetic_profile','write_count','exec_count','spawn_count'])
(w/'node-replay-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('12 synthetic traces passed; readable and obfuscated sources agree on all six scenarios.')
