#!/usr/bin/env python3
"""Check Sliver call-site variations and neutral message construction."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())

    def fixture(level, name):
        return (root / 'testdata' / level / 'go-bad-improve' / name).read_text()

    def previous(name):
        return (root / 'testdata/hostile/go-bad-review' / name).read_text()

    def documented(source):
        return 'package notes\n' + '\n'.join('// ' + line for line in source.splitlines()) + '\n'

    def aliases(source):
        for old, new in [('console', 'operator'), ('commonpb', 'reply'), ('sliverpb', 'wire'), ('licenses', 'legal')]:
            module = 'github.com/bishopfox/sliver/' + ('client/' if old in ['console', 'licenses'] else 'protobuf/') + old
            source = source.replace('"' + module + '"', new + ' "' + module + '"')
            source = source.replace(old + '.', new + '.')
        for old, new in [('con', 'controller'), ('rpc', 'service'), ('req', 'request'), ('resp', 'response')]:
            source = re.sub(r'\b' + old + r'\b', new, source)
        return source

    network = previous('rpc-network.go')
    license = previous('operator-licenses.go')
    monitor = fixture('hostile', 'monitor-assignment.go')
    response = fixture('notable', 'response-factory.go')
    cases = {
        'network-if.go': fixture('hostile', 'network-if-init.go'),
        'network-assignment.go': network.replace('err := rpc.GenericHandler', 'var err error\n\terr = rpc.GenericHandler'),
        'network-var.go': network.replace('err := rpc.GenericHandler', 'var err = rpc.GenericHandler'),
        'network-response-assignment.go': re.sub(r'resp := &sliverpb\.(Ifconfig|Netstat)\{', r'var resp *sliverpb.\1\n\tresp = &sliverpb.\1{', network),
        'network-response-var.go': network.replace('resp :=', 'var resp ='),
        'network-expression.go': network.replace('err := rpc.GenericHandler(req, resp)\n\tif err != nil {\n\t\treturn nil, err\n\t}', 'rpc.GenericHandler(req, resp)'),
        'monitor-assignment.go': monitor,
        'monitor-var.go': monitor.replace('var err error\n    _, err =', 'var _, err ='),
        'monitor-if.go': monitor.replace('var err error\n    _, err = con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{})\n    _ = err', 'if _, err := con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{}); err != nil { return }'),
        'monitor-expression.go': monitor.replace('var err error\n    _, err = con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{})\n    _ = err', 'con.Rpc.MonitorStart(context.Background(), &commonpb.Empty{})'),
        'monitor-return.go': monitor.replace('args []string) {', 'args []string) (any, error) {').replace('var err error\n    _, err = con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{})\n    _ = err', 'return con.Rpc.MonitorStop(context.Background(), &commonpb.Empty{})'),
        'license-var.go': fixture('hostile', 'license-var.go'),
        'license-assignment.go': license.replace('licensesCmd :=', 'var licensesCmd *cobra.Command\n\tlicensesCmd ='),
        'license-return.go': license.replace('[]*cobra.Command {', '*cobra.Command {').replace('licensesCmd :=', 'return').replace('\n\treturn []*cobra.Command{licensesCmd}', ''),
        'response-return.go': response,
        'response-variable.go': response.replace('return &commonpb.Response{}', 'var value = &commonpb.Response{}\n    return value'),
        'response-assignment.go': response.replace('return &commonpb.Response{}', 'var value *commonpb.Response\n    value = &commonpb.Response{}\n    return value'),
        'telegram.go': fixture('notable', 'telegram.go'),
        'telegram-alias.go': fixture('notable', 'telegram.go').replace('tgbotapi', 'botapi'),
    }
    network_names = {name for name in cases if name.startswith('network-')}
    monitor_names = {name for name in cases if name.startswith('monitor-')}
    license_names = {name for name in cases if name.startswith('license-')}
    for name in list(network_names | monitor_names | license_names):
        cases['alias-' + name] = aliases(cases[name])
    cases['other-network-receiver.go'] = cases['network-if.go'].replace('rpc.GenericHandler', 'other.GenericHandler')
    cases['other-network-request.go'] = cases['network-var.go'].replace('GenericHandler(req, resp)', 'GenericHandler(other, resp)')
    cases['other-network-module.go'] = cases['network-response-assignment.go'].replace('github.com/bishopfox/sliver/', 'example.org/operator/')
    cases['other-monitor-receiver.go'] = cases['monitor-if.go'].replace('con.Rpc.MonitorStop', 'other.Rpc.MonitorStop')
    cases['other-monitor-module.go'] = cases['monitor-var.go'].replace('github.com/bishopfox/sliver/', 'example.org/operator/')
    cases['other-license-member.go'] = cases['license-assignment.go'].replace('licenses.All', 'other.All')
    cases['other-license-module.go'] = cases['license-return.go'].replace('github.com/bishopfox/sliver/client/licenses', 'example.org/licenses')
    cases['other-response-module.go'] = response.replace('github.com/bishopfox/sliver/protobuf/commonpb', 'example.org/reply')
    for name in ['network-if.go', 'monitor-assignment.go', 'license-var.go', 'response-return.go', 'telegram.go']:
        cases['documented-' + name] = documented(cases[name])

    with tempfile.TemporaryDirectory(prefix='go-bad-improve-') as work:
        stage = Path(work) / 'source'
        stage.mkdir()
        for name, source in cases.items():
            (stage / name).write_text(source)
        proc = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', str(stage)],
                              text=True, capture_output=True, check=True)
        assert 'skipped' not in proc.stderr.lower(), proc.stderr
        reports = [json.loads(line) for line in proc.stdout.split('\n') if line]
        files = {Path(f['path']).name: f for r in reports for f in r['files']}
        assert files.keys() == cases.keys(), (files.keys(), cases.keys())
        family = 'well-known/malware/rat/sliver::'
        expected = {}
        for names, wanted in [
            (network_names, {family + 'sliver-network-rpc-server-source',
                             'objectives/discovery/network/interface::sliver-remote-ifconfig-tasking',
                             'objectives/discovery/network/enumeration::sliver-remote-netstat-tasking'}),
            (monitor_names, {family + 'sliver-operator-monitor-command-source'}),
            (license_names, {family + 'sliver-operator-license-command-source'}),
        ]:
            for name in names:
                expected[name] = expected['alias-' + name] = wanted
        for name, report in files.items():
            high = {t['id'] for t in report.get('traits', []) if t['crit'] >= 4}
            assert high == expected.get(name, set()), (name, high, expected.get(name, set()))
            assert all(t['crit'] == 5 for t in report.get('traits', []) if t['id'] in high), name
        def ids(name):
            return {t['id'] for t in files[name].get('traits', [])}
        response_id = 'micro-behaviors/data/serialize/protobuf::go-sliver-response-envelope'
        for name in ['response-return.go', 'response-variable.go', 'response-assignment.go']:
            assert response_id in ids(name), name
        for name in ['other-response-module.go', 'documented-response-return.go']:
            assert response_id not in ids(name), name
        construction = {'micro-behaviors/communications/messaging/create::go-bot-api-constructor-call',
                        'micro-behaviors/communications/messaging/create::go-message-constructor-call'}
        for name in ['telegram.go', 'telegram-alias.go']:
            assert construction <= ids(name), (name, construction - ids(name))
        assert not construction & ids('documented-telegram.go')
    print(f'Go bad-label improvement regressions passed: {len(cases)} controls; no sample code executed')


if __name__ == '__main__':
    main()
