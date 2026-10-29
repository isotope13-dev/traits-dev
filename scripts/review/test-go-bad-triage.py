#!/usr/bin/env python3
"""Check Sliver source identities, neutral message sinks, and quoted shell data."""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave',default='../cleave/target/release/cleave')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    cleave=str(Path(args.cleave).resolve())

    def fixture(level,name):
        return (root/'testdata'/level/'go-bad-review'/name).read_text()

    def documented(source):
        return 'package notes\n'+'\n'.join('// '+line for line in source.splitlines())+'\n'

    def rename(source):
        for old,alias in [('console','operator'),('commonpb','reply'),('sliverpb','wire'),('licenses','legal')]:
            module='github.com/bishopfox/sliver/'+('client/' if old in ['console','licenses'] else 'protobuf/')+old
            source=source.replace('"'+module+'"',alias+' "'+module+'"')
            source=source.replace(old+'.',alias+'.')
        for old,new in [('con','controller'),('rpc','service'),('req','request'),('resp','response')]:
            source=re.sub(r'\b'+old+r'\b',new,source)
        for old,new in [('MonitorStartCmd','begin'),('MonitorStopCmd','finish'),('Commands','register'),('Ifconfig','networkInfo'),('Netstat','socketInfo')]:
            # Rename local declarations, retaining the protobuf API types.
            source=re.sub(r'(?<=func )'+old+r'\b',new,source)
            source=re.sub(r'(func \([^)]*\) )'+old+r'\b',r'\g<1>'+new,source)
        return source

    cases={}
    originals=['rpc-network.go','operator-licenses.go','operator-monitor-start.go','operator-monitor-stop.go']
    for name in originals:
        source=fixture('hostile',name)
        cases[name]=source
        cases['renamed-'+name]=rename(source)
        cases['documented-'+name]=documented(source)
        cases['other-module-'+name]=source.replace('github.com/bishopfox/sliver/','example.org/operator/')
    rpc=cases['rpc-network.go']
    cases['rpc-other-receiver.go']=rpc.replace('rpc.GenericHandler(req, resp)','other.GenericHandler(req, resp)')
    cases['rpc-other-request.go']=rpc.replace('rpc.GenericHandler(req, resp)','rpc.GenericHandler(other, resp)')
    cases['rpc-other-response.go']=rpc.replace('github.com/bishopfox/sliver/protobuf/commonpb','example.org/response/commonpb')
    cases['rpc-no-dispatch.go']=rpc.replace('rpc.GenericHandler(req, resp)','localCheck(req, resp)')
    cases['operator-unrelated-monitor.go']=cases['operator-monitor-start.go'].replace('con.Rpc.MonitorStart','other.Rpc.MonitorStart')
    cases['operator-no-monitor.go']=cases['operator-monitor-start.go'].replace('con.Rpc.MonitorStart','con.Rpc.Check')
    cases['operator-unrelated-license.go']=cases['operator-licenses.go'].replace('licenses.All','other.All')
    cases['operator-other-license-module.go']=cases['operator-licenses.go'].replace('github.com/bishopfox/sliver/client/licenses','example.org/licenses')
    cases['operator-type-only.go']='''package helper
import "github.com/bishopfox/sliver/client/console"
func use(client *console.SliverClient) {}
'''
    sinks={'push-sms.go':'push-sms','send-text.go':'send-text-message','direct-message.go':'direct-message-event',
           'post-message.go':'post-message-context','notify-message.go':'notify-message','message-event.go':'send-message-event',
           'push-note.go':'push-note','push-message.go':'push-message'}
    for name in sinks:
        source=fixture('notable',name)
        cases[name]=source
        cases['documented-'+name]=documented(source)
    for level,name in [('baseline','image-command-history.json'),('baseline','escaped-address-example.json'),
                       ('suspicious','address-substitution.json'),('suspicious','interface-substitution.json')]:
        cases[name]=fixture(level,name)
    cases['plain-address.json']='{"Ip":"192.0.2.1"}\n'
    cases['source-address.py']='payload = {"Ip": "$(id)"}\n'

    with tempfile.TemporaryDirectory(prefix='go-bad-review-') as work:
        stage=Path(work)/'source'
        stage.mkdir()
        for name,source in cases.items():
            (stage/name).write_text(source)
        result=subprocess.run([cleave,'--traits-dir',str(root),'--format','jsonl',str(stage)],capture_output=True,text=True,check=True)
        assert 'skipped' not in result.stderr.lower(),result.stderr
        reports=[json.loads(line) for line in result.stdout.split('\n') if line]
        files={Path(f['path']).name:f for report in reports for f in report['files']}
        assert files.keys()==cases.keys(),(files.keys(),cases.keys())

        def ids(name):
            return {t['id'] for t in files[name].get('traits',[])}

        family='well-known/malware/rat/sliver::'
        network={family+'sliver-network-rpc-server-source',
                 'objectives/discovery/network/interface::sliver-remote-ifconfig-tasking',
                 'objectives/discovery/network/enumeration::sliver-remote-netstat-tasking'}
        allowed_high={}
        for name in originals:
            wanted=network if name=='rpc-network.go' else {family+('sliver-operator-license-command-source' if name=='operator-licenses.go' else 'sliver-operator-monitor-command-source')}
            for prefix in ['','renamed-']:
                allowed_high[prefix+name]=wanted
        json_trait='objectives/execution/exploit/command-injection::json-address-field-shell-substitution'
        allowed_high['address-substitution.json']={json_trait}
        allowed_high['interface-substitution.json']={json_trait}
        allowed_high['source-address.py']={'objectives/execution/exploit/command-injection::address-field-shell-substitution'}
        for name,file in files.items():
            high={t['id'] for t in file.get('traits',[]) if t['crit']>=4}
            assert high==allowed_high.get(name,set()),(name,high,allowed_high.get(name,set()))
            if name in allowed_high and name.endswith('.go'):
                assert all(t['crit']==5 for t in file['traits'] if t['id'] in high),name
        for name,key in sinks.items():
            wanted='micro-behaviors/communications/messaging/send::go-'+key+'-helper-call'
            assert wanted in ids(name),(name,wanted)
            assert wanted not in ids('documented-'+name),(name,wanted)
    print(f'Go bad-triage regressions passed: {len(cases)} controls; no sample code executed')


if __name__=='__main__':
    main()
