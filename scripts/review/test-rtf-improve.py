#!/usr/bin/env python3
"""Check document observations, bound field commands, and RTF exploit variants."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
DDE = 'objectives/execution/interpreter/document/command::rtf-ddeauto-shell-execution'
SHAPE = 'objectives/execution/exploit/document::rtf-shape-property-overflow'
PROPERTY = 'metadata/document/rtf/properties::rtf-pfragments-property-declaration'
OBJECT = 'metadata/document/rtf/ole::object-control-feature'
REMOTE = 'metadata/document/rtf/properties::http-includetext-instruction'
IMPORT = 'metadata/document/rtf/properties::http-import-instruction'
LONG_CONTROL = 'metadata/document/rtf/structure::oversized-alphabetic-control-word'
TEMPLATE = 'micro-behaviors/fs/path/extension::word-template-extension-reference'
CERT = 'micro-behaviors/fs/path/application/browser/profile::firefox-cert9-database-reference'
RANGE = 'micro-behaviors/data/document/spreadsheet::vba-worksheet-range-value-reference'
DIALOG = 'micro-behaviors/ui/dialog/message::vbs-frequent-message-box-calls'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='../cleave/target/release/cleave')
    ap.add_argument('--decoded-samples', type=Path)
    args = ap.parse_args()
    cases = {}

    def add(name, source, required=(), forbidden=(), hostile=False):
        data = source.encode() if isinstance(source, str) else source
        cases[name] = (data, set(required), set(forbidden), hostile)

    def rtf(body):
        return r'{\rtf1\ansi ' + body + '}'

    def field(kind, target):
        return '{\\field{\\*\\fldinst ' + kind + ' ' + target + '}{\\fldrslt text}}'

    for app in ['cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe', 'mshta.exe', 'bitsadmin.exe']:
        add('dde-'+app+'.rtf', rtf(field('DDEAUTO', app+' /c harmless')), [DDE], hostile=True)
    add('dde-quoted-path.rtf', rtf(field('DDEAUTO', r'"C:\Windows\System32\cmd.exe" /c echo test')), [DDE], hostile=True)
    add('dde-bare-shell.rtf', rtf(field('DDEAUTO', 'cmd /c echo test')), [DDE], hostile=True)
    add('dde-nested-instruction.rtf', rtf('{\\field{\\*\\fldinst{DDEAUTO cmd.exe /c echo test}}}'), [DDE], hostile=True)
    add('dde-excel-plus-shell-link.rtf', rtf(field('DDEAUTO', 'Excel Sheet1')+field('HYPERLINK', '"https://example.invalid/cmd.exe"')), forbidden=[DDE])
    add('dde-excel-plus-utility-link.rtf', rtf(field('DDEAUTO', 'Excel Sheet1')+field('HYPERLINK', '"https://example.invalid/powershell"')), forbidden=[DDE])
    add('dde-prose-command.rtf', rtf('DDEAUTO cmd.exe is documentation. '+field('DDEAUTO', 'Excel Sheet1')), forbidden=[DDE])
    add('dde-noncommand-extension.rtf', rtf(field('DDEAUTO', 'cmd.exe.manifest')), forbidden=[DDE])
    add('remote-include.rtf', rtf(field('INCLUDETEXT', '"https://example.invalid/report.rtf"')), [REMOTE], ['objectives/execution/interpreter/document/command::rtf-template-injection-remote'])
    add('remote-import.rtf', rtf(field('IMPORT', '"http://example.invalid/report.rtf"')), [IMPORT])
    add('pandoc-9.rtf', rtf(field('HYPERLINK', '"https://example.invalid/"')), ['metadata/document/rtf/properties::rtf-field-target-remote-url'])
    add('local-include-remote-link.rtf', rtf(field('INCLUDETEXT', '"local.rtf"')+field('HYPERLINK', '"https://example.invalid/"')), forbidden=[REMOTE, IMPORT])
    add('local-import-remote-link.rtf', rtf(field('IMPORT', '"local.rtf"')+field('HYPERLINK', '"https://example.invalid/"')), forbidden=[REMOTE, IMPORT])
    signature = 'd0cf11e0a1b11ae1'
    linked = r'{\object\objautlink\objupdate{\*\objclass Word.Document.8}{\*\objdata '+signature+'}}'
    add('ordinary-linked-object.rtf', rtf(linked), [OBJECT])
    add('linked-object-with-nuls.rtf', rtf(linked).encode()+b'\x00\x00\x00', [OBJECT, 'metadata/document/rtf/ole::word-class-autolink-controls-null-bytes'])
    add('ordinary-activex.rtf', rtf(r'{\object\objocx{\*\objclass Example.Control}{\*\objdata '+signature+'}}'), [OBJECT, 'metadata/document/rtf/ole::activex-and-compound-data'])
    add('malformed-auto-update.rtf', rtf(r'{\object123456789012345678\objupdate{\*\objdata '+signature+'}}'), ['objectives/execution/exploit/document::rtf-hex-ole-overflow-autoload'], hostile=True)
    buf = '41'*180
    for name in ['pFragments', 'pFraments', 'PFRAGMENTS']:
        for reverse in [False, True]:
            prop = r'{\sn '+name+'}'
            value = '{\\sv\t1;1;'+buf+'}'
            body = r'{\shp{\sp'+(value+prop if reverse else prop+value)+'}}'
            add(f'shape-{name}-{reverse}.rtf', rtf(body), [PROPERTY, SHAPE], hostile=True)
    add('shape-invalid-element-size.rtf', rtf(r'{\shp{\sp{\sn pFragments}{\sv 1;X;'+buf+'}}}'), [PROPERTY, SHAPE], hostile=True)
    add('shape-small.rtf', rtf(r'{\shp{\sp{\sn pFragments}{\sv 1;1;41}}}'), [PROPERTY], [SHAPE])
    add('shape-prose-name.rtf', rtf('pFragments is a property. '+r'{\shp{\sp{\sn Other}{\sv 1;1;'+buf+'}}}'), forbidden=[PROPERTY, SHAPE])
    add('shape-unrelated-properties.rtf', rtf(r'{\shp{\sp{\sn pFragments}{\sv 1;1;41}}{\sp{\sn Other}{\sv 1;1;'+buf+'}}}'), [PROPERTY], [SHAPE])
    add('large-control.rtf', '{\\'+'A'*600+'}', [LONG_CONTROL])
    add('escaped-long-word.rtf', rtf('\\\\'+'A'*600), forbidden=[LONG_CONTROL])
    add('ordinary-control.rtf', rtf(r'\pard\plain text'), forbidden=[LONG_CONTROL])
    add('template-extension.rtf', rtf(r'Office\Report.DOTM'), [TEMPLATE])
    add('dotcom-domain.rtf', rtf('https://example.dotcom.invalid'), forbidden=[TEMPLATE])
    add('list-template-control.rtf', rtf(r'\listtemplateid123 text'), forbidden=['metadata/document/rtf/properties::template-control-reference'])
    add('template-control.rtf', rtf(r'{\template report.dot}'), ['metadata/document/rtf/properties::template-control-reference', TEMPLATE])
    add('certificate-profile.c', 'const char *allowed = "/home/alice/.mozilla/firefox/profile/cert9.db";\n', [CERT], ['objectives/credential-access/browser/firefox::cert9-db'])
    add('worksheet-value.vbs', 'Sub Main()\nvalue = Worksheets(1).Range("D15").Value\nEnd Sub\n', [RANGE], ['micro-behaviors/data/document/spreadsheet::vba-worksheet-range-byte-source'])
    add('many-handlers.vbs', '\n'.join(f'Sub Case{i}()\n MsgBox("status")\nEnd Sub\n' for i in range(35)), [DIALOG], ['objectives/evasion/anti-av/code-padding::dense-message-box-padding'])
    resolver = '813e4765745075f2817e04726f634175e98b752403f3668b14568b751c03f3'
    obj = r'{\object\objocx{\*\objclass MSComctlLib.ListViewCtrl.2}{\*\objdata '+signature+resolver+'}}'
    add('listview-with-code.rtf', rtf(obj), ['objectives/execution/exploit/document::rtf-listview-api-resolving-shellcode'], hostile=True)
    add('reflowed-listview-code.rtf', rtf(obj.replace(resolver, '\n'.join(resolver[i:i+4] for i in range(0, len(resolver), 4)))), ['objectives/execution/exploit/document::rtf-listview-api-resolving-shellcode'], hostile=True)
    add('listview-without-code.rtf', rtf(obj.replace(resolver, '00')), ['metadata/document/rtf/ole::mscomctl-listview-control-class'])
    add('code-without-listview.rtf', rtf(obj.replace('MSComctlLib.ListViewCtrl.2', 'Example.Control')), ['micro-behaviors/os/api-resolution/manual::hex-x86-getprocaddress-export-walk'])
    add('distant-resolver-fragments.rtf', rtf(obj.replace('75f2', '00'*200+'75f2')))
    if args.decoded_samples:
        for sample in ['CVE-2010-3333-1.rtf', 'CVE-pseudo-2009-0238-1.rtf']:
            p = next(args.decoded_samples.rglob(sample))
            add('real-'+sample, p.read_bytes(), [SHAPE], hostile=True)
        p = next(args.decoded_samples.rglob('EDB-38031-1.rtf'))
        add('real-listview-shellcode.rtf', p.read_bytes(), ['objectives/execution/exploit/document::rtf-listview-api-resolving-shellcode'], hostile=True)
        p = next(args.decoded_samples.rglob('CVE-2005-2971-1.rtf'))
        add('real-long-control.rtf', p.read_bytes(), [LONG_CONTROL])
    with tempfile.TemporaryDirectory(prefix='rtf-improve-controls-') as tmp:
        work = Path(tmp)
        for name, (data, *_rest) in cases.items():
            (work/name).write_bytes(data)
        r = subprocess.run([str((ROOT/args.cleave).resolve()), '--traits-dir', str(ROOT), '--format', 'json', str(work)], text=True, capture_output=True, check=True)
        files = {Path(f['path']).name: f for line in r.stdout.split('\n') if line.strip() for f in json.loads(line)['files']}
        for name, (_data, required, forbidden, hostile) in cases.items():
            traits = files[name].get('traits', [])
            ids = {t['id'] for t in traits}
            assert not required-ids, (name, 'missing', required-ids)
            assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
            attacks = {t['id'] for t in traits if t['crit'] == 5}
            assert bool(attacks) == hostile, (name, 'hostile', attacks, hostile)
            print('PASS', name)
    print(f'{len(cases)} RTF improvement controls passed')


if __name__ == '__main__':
    main()
