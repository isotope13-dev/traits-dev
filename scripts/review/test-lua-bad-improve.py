#!/usr/bin/env python3
"""Check Lua finding claims against connected and unrelated evidence; never execute samples."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    fixture = 'generated/taxonomy/lua-triage-bad-20261102'
    hostile = repo/'testdata/hostile'/fixture
    notable = repo/'testdata/notable'/fixture
    phish = (hostile/'http-phish.lua').read_text()
    spec = (notable/'language-spec.lua').read_text()
    worm = (hostile/'worm.vbs').read_text()
    hook = (hostile/'Jamfile.lua').read_text()
    secret = 'objectives/exfiltration/stealer/credential/raw-file::lua-secret-file-http-upload'
    phishing = 'objectives/credential-access/phishing/mfa::lua-mfa-phishing-terminal-delivery'
    lure_pipe = 'objectives/credential-access/phishing/mfa::lua-mfa-lure-to-process-input'
    native = 'micro-behaviors/process/deploy/interpreter-command::lua-module-native-interpreter-helper'
    hidden = 'micro-behaviors/ui/window/visibility::lua-hide-window-call'
    concealed = 'objectives/execution/payload/file-exec/command/fetch::lua-concealed-curl-batch-stage'
    mail = 'objectives/lateral-movement/worm/email::wsh-outlook-address-mailer'
    cases = {}

    def add(name, content, *, yes=(), no=(), elevated=False):
        cases[name] = (content, set(yes), set(no), elevated)

    add('secret-source-to-http.lua', phish, yes={secret, phishing, lure_pipe}, elevated=True)
    add('renamed-source-field.lua', phish.replace('{ path =', '{ location =').replace('source.path', 'source.location'), yes={secret}, elevated=True)
    add('commented-read-boundary.lua', phish.replace('f:close()\n            if content', 'f:close()\n            -- keep the same read result\n            if content'), yes={secret}, elevated=True)
    public = '''local names={"/.netrc","/.ssh/id_rsa"}
local http=require("socket.http")
local f=io.open("public-report.txt","r")
local body=f:read("*a")
http.request("https://reports.example.invalid",body)
'''
    add('unrelated-secret-names.lua', public, no={secret})
    add('unrelated-secret-fields.lua', public.replace('local names={"/.netrc","/.ssh/id_rsa"}', 'local names={{path="/.netrc"},{path="/.ssh/id_rsa"}}'), no={secret})
    add('wrong-source-collection.lua', phish.replace('ipairs(credential_sources)', 'ipairs(public_sources)'), no={secret, phishing}, elevated=True)
    add('wrong-source-field.lua', phish.replace('io.open(source.path, "r")', 'io.open(source.public_path, "r")'), no={secret}, elevated=True)
    add('different-read-receiver.lua', phish.replace('local content = f:read("*a")', 'local content = report:read("*a")'), no={secret}, elevated=True)
    add('status-body-instead-of-file.lua', phish.replace('http.request(url, content, request_headers)', 'http.request(url, "status=ready", request_headers)'), no={secret}, elevated=True)
    add('overwritten-file-body.lua', phish.replace('f:close()\n            if content', 'f:close()\n            content="status=ready"\n            if content'), no={secret}, elevated=True)
    add('unrelated-lure-write.lua', phish.replace('handle:write(message)', 'handle:write("diagnostic")'), yes={secret}, no={phishing, lure_pipe}, elevated=True)
    add('printed-lure-not-piped.lua', phish.replace('io.popen(tool ..', 'print(tool ..'), yes={secret}, no={phishing, lure_pipe}, elevated=True)
    add('ordinary-mfa-terminal-helper.lua', '''local text=string.format("Continue by entering your MFA token at https://identity.example.invalid",user)
local handle=io.popen("/bin/write operator")
handle:write(text)
''', yes={lure_pipe}, no={phishing})
    add('editor-worker.lua', spec, yes={native})
    add('printed-editor-command.lua', spec.replace('createProcess([[', 'print([['), no={native})
    add('unused-editor-helper.lua', spec.replace('createProcess([["bin', 'otherHelper([["bin'), no={native})
    add('renamed-editor-helper.lua', spec.replace('createProcess', 'launch_worker').replace('user-data.lua', 'index-worker.lua'), yes={native})
    add('commented-editor-invocation.lua', spec.replace('createProcess([["bin', '-- createProcess([["bin'), no={native})
    add('direct-zero.lua', 'ffi.C.ShowWindow(h,0)\n', yes={hidden})
    add('hex-zero.lua', 'ffi.C.ShowWindow(h,0x0)\n', yes={hidden})
    add('renamed-zero-alias.lua', 'local mode=0\nlocal renamed=mode\nffi.C.ShowWindow(h,renamed)\n', yes={hidden})
    add('nested-zero.lua', 'function hide() local mode=0; print("starting"); ffi.C.ShowWindow(h,mode) end\n', yes={hidden})
    add('reassigned-nonzero.lua', 'local mode=0\nmode=1\nffi.C.ShowWindow(h,mode)\n', no={hidden})
    add('reassigned-zero.lua', 'local mode=1\nmode=0\nffi.C.ShowWindow(h,mode)\n', yes={hidden})
    add('zero-operand-not-mode.lua', 'local mode=0+1\nffi.C.ShowWindow(h,mode)\n', no={hidden})
    add('zero-string.lua', 'ffi.C.ShowWindow(h,"0")\n', no={hidden})
    add('zero-in-other-argument.lua', 'ffi.C.ShowWindow(0,1)\n', no={hidden})
    add('window-flag-overwritten-stage.lua', hook.replace('if hWnd ~= nil then', 'SW_HIDE=1\nif hWnd ~= nil then'), no={hidden, concealed}, elevated=True)
    add('mail-worm.vbs', worm, yes={mail}, elevated=True)
    add('worm-without-send.vbs', '\n'.join(line for line in worm.split('\n') if line.strip().lower()!='male.send'), no={mail}, elevated=True)
    add('worm-without-attachment.vbs', '\n'.join(line for line in worm.split('\n') if 'male.Attachments.Add' not in line), no={mail}, elevated=True)
    add('draft-only.vbs', '''Sub BuildDraft(outlook, mail)
Set ns=outlook.GetNameSpace("MAPI")
count=ns.AddressLists.Count
mail.Recipients.Add "editor@example.invalid"
End Sub
''', no={mail})
    add('ordinary-outlook-reports.vbs', '''Sub Reports(outlook,mail)
Set ns=outlook.GetNameSpace("MAPI")
For i=1 To ns.AddressLists.Count
mail.Recipients.Add ns.AddressLists(i)
mail.Attachments.Add "public-report.csv"
mail.Send
Next
End Sub
''', no={mail})
    add('password-documentation.lua', '-- Documentation: harvest password requirements for policy reports\nreturn {}\n', yes={'metadata/lang/natural/credential::password-acquisition-wording'}, no={'objectives/credential-access/theft/authentication/keywords::password'})
    add('proc-status-field.lua', 'return "TracerPid"\n', yes={'micro-behaviors/process/debug/detect::script-tracerpid-field-reference'}, no={'objectives/anti-analysis/debugger-detect/check::tracerpid-string'})
    mount = 'micro-behaviors/fs/file/copy/source-destination::lua-script-copy-to-discovered-mount'
    solaris = (hostile/'solaris.lua').read_text()
    add('mounted-script-copy.lua', solaris, yes={mount}, elevated=True)
    add('renamed-mounted-script.lua', solaris.replace('worm.sh', 'stage-job.sh').replace('mount_point', 'mounted_root'), yes={mount}, elevated=True)
    add('printed-mounted-script.lua', solaris.replace('    run(', '    print('), no={mount}, elevated=True)
    decoder = 'local packed={' + ','.join('"' + '\\065'*96 + '"' for _ in range(160)) + '}\n'
    decoder += 'local function unpack_byte(n,o) local x=n*64^(3-o);return math.floor(x/65536),math.floor((x%65536)/256) end\n'
    decoder += 'return {data=packed,decode=unpack_byte,environment=getfenv(),proxy=newproxy,meta=setmetatable}\n'
    for name, worker, unusual in [('plain-editor-bundle.zip', 'return {worker=true}\n', False),
                                   ('concealed-editor-worker.zip', decoder, True)]:
        archive = io.BytesIO()
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as out:
            out.writestr('spec/language.lua',spec)
            out.writestr('cfg/user-data.lua',worker)
        add(name,archive.getvalue(),no={'objectives/supply-chain/impersonation/editor::lua-editor-concealed-sidecar-bundle'}, elevated=unusual)
    with tempfile.TemporaryDirectory(prefix='lua-bad-improve-controls-') as directory:
        work = Path(directory)
        for name, (source, _, _, _) in cases.items():
            (work/name).write_bytes(source if isinstance(source,bytes) else source.encode())
        result = subprocess.run([str((repo/args.cleave).resolve()), '--traits-dir', str(repo), '--all-files', '--format=json', str(work)],
                                check=True, capture_output=True, text=True)
        assert 'skipped trait file' not in result.stderr, result.stderr
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        roots = {Path(report['files'][0]['path']).name:report['files'][0] for report in reports}
        assert set(cases) <= roots.keys(), set(cases)-roots.keys()
        for name, (_, required, forbidden, allow_elevated) in cases.items():
            traits = roots[name].get('traits',[])
            ids = {t['id'] for t in traits}
            assert required <= ids, (name, required-ids)
            assert not forbidden & ids, (name, forbidden & ids)
            if name in {'plain-editor-bundle.zip', 'concealed-editor-worker.zip'}:
                assert not [t['id'] for t in traits if t['crit']>=5], (name, [t['id'] for t in traits if t['crit']>=5])
            if not allow_elevated:
                assert not [t['id'] for t in traits if t['crit']>=4], (name, [t['id'] for t in traits if t['crit']>=4])
            print('PASS',name)
    print(f'{len(cases)} Lua improvement controls passed')


if __name__ == '__main__':
    main()
