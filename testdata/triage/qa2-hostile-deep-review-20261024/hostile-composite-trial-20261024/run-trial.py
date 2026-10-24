from pathlib import Path
import json,subprocess,os,hashlib
W=Path('/tmp/qa2-hostile-composites');ROOT=Path('/home/t/src/traits-dev')
CFG='objectives/command-and-control/infrastructure/endpoint::trial-commonjs-init-collector-config'
INI='objectives/execution/exploit/module-config::trial-standalone-rce-module-config'
CFGP='micro-behaviors/communications/http/url/php-endpoint::external-ip-php-init-query-correlation'
INIP='metadata/file/catalog/exploit::exploit-catalog-rce-declaration'
source_cfg=Path('/tmp/qa2-deep-review/inputs/bc15c52b714c78368a5dbc5b8f22ccba230ae76bfded55fd75864b0ddda9f01a/cfg.js').read_text()
source_ini=Path('/tmp/qa2-deep-review/inputs/49131075d5210a85c6080519c7931c09446d42bf06c14cfc2d3d857b213b209d/003.ini').read_text()
cases=[]
def case(name,body,basename,expected_class,candidate,profile):
    p=W/'inputs'/name/basename;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
    cases.append({'case':name,'path':str(p),'expected_class':expected_class,'candidate':candidate,'profile':profile,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
case('actual-config',source_cfg,'settings.js','likely hostile',CFG,CFGP)
case('renamed-config-variant',source_cfg.replace('217.197.107.91','185.199.108.153').replace('login.php','status.php').replace('dGVzdA==','bm9kZTE='),'bootstrap.js','likely hostile',CFG,CFGP)
# Synthetic legitimate counterpart: an operator-configured public-IP PHP
# service with an optional mirror, an initialization ID, and a data argument.
# The consumer sends a fixed application version and interprets no commands.
# This is a constructed counterexample, not a claim about a real vendor/IP.
telemetry=source_cfg.replace('217.197.107.91','93.184.215.14').replace('dGVzdA==','ZGVtbw==')
case('benign-service-config',telemetry,'service.js','benign synthetic service configuration',CFG,CFGP)
case('normal-domain-service',telemetry.replace('93.184.215.14','service.example'),'service.js','benign synthetic service configuration',CFG,CFGP)
case('private-service-config',telemetry.replace('93.184.215.14','192.168.50.2'),'service.js','benign synthetic service configuration',CFG,CFGP)
case('actual-descriptor',source_ini,'entry.ini','likely hostile',INI,INIP)
case('renamed-descriptor-variant',source_ini.replace('javagetval','alternate_jvm_entry'),'entry.ini','likely hostile',INI,INIP)
# The same minimal fields can be one entry in an authorized scanner's
# vulnerability/reproduction inventory. No exploit implementation is supplied.
catalog=source_ini.replace('javagetval','jvm_getvalue_inventory')
case('benign-research-catalog',catalog,'entry.ini','benign synthetic research catalog record',INI,INIP)
case('ordinary-java-inventory',catalog.replace('Java getValue Remote Code Execution','Java runtime version inventory'),'entry.ini','benign inventory',INI,INIP)
case('descriptive-prose','This document describes Java remote code execution.\n','entry.ini','benign documentation',INI,INIP)
(W/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
for mode,traits in [('candidate',W/'traits'),('production',ROOT)]:
    run=subprocess.run([str(ROOT.parent/'cleave/target/release/cleave'),'--traits-dir',str(traits),'analyze','--format','jsonl',*[r['path'] for r in cases]],capture_output=True,text=True,env={**os.environ,'CLEAVE_SKIP_CACHE':'1'})
    (W/(mode+'-scan.jsonl')).write_text(run.stdout);(W/(mode+'-scan.stderr')).write_text(run.stderr)
    assert run.returncode==0,run.stderr[-2000:]
    by={r['files'][0]['path']:r for r in map(json.loads,run.stdout.splitlines()) if r.get('files')};results=[]
    for case_row in cases:
        fs=by[case_row['path']]['files'];ts={t['id']:t['crit'] for f in fs for t in f.get('traits',[])}
        row={**case_row,'hostile':sum(c==5 for c in ts.values()),'suspicious':sum(c==4 for c in ts.values()),'candidate_matches':ts.get(case_row['candidate'])==5,'profile_matches':case_row['profile'] in ts,'high_traits':[{'id':i,'criticality':c} for i,c in sorted(ts.items()) if c>=4]}
        results.append(row);print(mode,row['case'],'H',row['hostile'],'S',row['suspicious'],'candidate',row['candidate_matches'],flush=True)
    (W/(mode+'-results.json')).write_text(json.dumps(results,indent=2)+'\n')
print('Trial complete; inspect benign-candidate collisions before admitting a rule.',flush=True)
