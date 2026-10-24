from pathlib import Path
import json,os,subprocess,tempfile
ROOT=Path('/home/t/src/traits-dev')
WORK=Path('/tmp/qa2-content-profiles')
REVIEW=ROOT/'testdata/triage/qa2-hostile-deep-review-20261024'
CFG='micro-behaviors/communications/http/url/php-endpoint::external-ip-php-init-query-correlation'
INI='metadata/file/catalog/exploit::exploit-catalog-rce-declaration'
samples=json.loads(Path('/tmp/qa2-deep-review/samples.json').read_text())
cfg=next(Path(r['analysis_path']).read_text() for r in samples if r['sha256'].startswith('bc15'))
ini=next(Path(r['analysis_path']).read_text() for r in samples if r['sha256'].startswith('491310'))
cases=[]
with tempfile.TemporaryDirectory(prefix='endpoint-content-profiles-') as scratch:
    scratch=Path(scratch)
    def case(name,body,basename,required=(),forbidden=(),max_susp=None,hostile=0):
        p=scratch/name/basename;p.parent.mkdir(parents=True);p.write_text(body)
        cases.append((name,p,set(required),set(forbidden),max_susp,hostile))
    for r in samples:
        sha=r['sha256'];required=[]
        h=next((count for prefix,count in [('201707',2),('311006',2),('aab86',1),('2e5c',3),('7e916',1)] if sha.startswith(prefix)),0)
        if sha.startswith('bc15'):required=[CFG]
        if sha.startswith('491310'):required=[INI]
        good=sha.startswith(('67a031','7b5c4','eeab0','a03f0','e60f5','2c4645'))
        cases.append((sha[:12],Path(r['analysis_path']),set(required),set(),1 if good else None,h))
    case('cfg-renamed-config',cfg,'settings.js',[CFG])
    case('cfg-other-ip-path-id',cfg.replace('217.197.107.91','185.199.108.153').replace('login.php','status.php').replace('dGVzdA==','bm9kZTE='),'settings.js',[CFG])
    case('cfg-no-init',cfg.replace('event=init','event=ordinary'),'settings.js',forbidden=[CFG],max_susp=1)
    case('cfg-no-encoded-id',cfg.replace('&id=dGVzdA==',''),'settings.js',forbidden=[CFG],max_susp=1)
    case('cfg-no-data-field',cfg.replace('&data=',''),'settings.js',forbidden=[CFG],max_susp=1)
    case('cfg-private-ip',cfg.replace('217.197.107.91','192.168.50.2'),'settings.js',forbidden=[CFG],max_susp=0)
    case('cfg-normal-domain',cfg.replace('217.197.107.91','api.service.example'),'settings.js',forbidden=[CFG],max_susp=0)
    case('cfg-ordinary-php-query',cfg.replace('event=init&id=dGVzdA==&data=','action=status'),'settings.js',forbidden=[CFG],max_susp=1)
    # The rule promises bounded co-occurrence, not same-value data flow.
    # Distant evidence must not satisfy that bounded correlation.
    distant='const a="http://185.199.108.153/status.php?action=status";\n'+('// padding\n'*100)+'const b="?event=init&id=bm9kZTE=&data=";'
    case('cfg-distant-correlation',distant,'settings.js',forbidden=[CFG],max_susp=1)
    case('ini-renamed-file',ini,'component.ini',[INI],max_susp=1)
    case('ini-different-module',ini.replace('javagetval','alternate_jvm_entry'),'component.ini',[INI],max_susp=1)
    case('ini-abbreviated-rce',ini.replace('Java getValue Remote Code Execution','Java RCE'),'component.ini',[INI],max_susp=1)
    case('ini-no-exploit-section',ini.replace('[exploit]','[documentation]'),'component.ini',forbidden=[INI],max_susp=0)
    case('ini-no-rce',ini.replace('Java getValue Remote Code Execution','Java version inventory'),'component.ini',forbidden=[INI],max_susp=0)
    case('ini-no-name',ini.replace('name="javagetval"',''),'component.ini',forbidden=[INI],max_susp=0)
    case('ini-no-description',ini.split('desc=')[0],'component.ini',forbidden=[INI],max_susp=0)
    case('ini-prose-mention','This document discusses Java Remote Code Execution.\n','component.ini',forbidden=[INI],max_susp=0)
    run=subprocess.run([str(ROOT.parent/'cleave/target/release/cleave'),'--traits-dir',str(ROOT),'analyze','--format','jsonl',*[str(c[1]) for c in cases]],text=True,capture_output=True,env={**os.environ,'CLEAVE_SKIP_CACHE':'1'})
    assert run.returncode==0,run.stderr
    (WORK/'scan.jsonl').write_text(run.stdout);(WORK/'scan.stderr').write_text(run.stderr)
    reports={r['files'][0]['path']:r for r in map(json.loads,run.stdout.splitlines()) if r.get('files')}
    results=[]
    for name,p,required,forbidden,max_susp,h_expected in cases:
        r=reports[str(p)]
        ts={t['id']:t['crit'] for f in r['files'] for t in f.get('traits',[])}
        missing=sorted(required-ts.keys());unexpected=sorted(forbidden & ts.keys())
        h=sum(c==5 for c in ts.values());s=sum(c==4 for c in ts.values())
        wrong_level=sorted(i for i in required if ts.get(i)!=4)
        passed=not missing and not unexpected and not wrong_level and h==h_expected and (max_susp is None or s<=max_susp)
        results.append({'case':name,'passed':passed,'missing':missing,'unexpected':unexpected,'wrong_level':wrong_level,'hostile':h,'suspicious':s,'high_traits':[{'id':i,'criticality':c} for i,c in sorted(ts.items()) if c>=4]})
        print('PASS' if passed else 'FAIL',name,'H',h,'S',s,missing,unexpected,wrong_level,flush=True)
    (WORK/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    assert all(r['passed'] for r in results)
print(len(results),'content-profile checks passed')
