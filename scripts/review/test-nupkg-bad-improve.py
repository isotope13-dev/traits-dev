#!/usr/bin/env python3
"""Check managed build-task capabilities without executing the task assembly."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    parser.add_argument('--samples-root', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    process = 'micro-behaviors/process/create/subprocess/launch::dotnet-process-start-call'
    directory = 'micro-behaviors/fs/delete/directory::dotnet-directory-delete-call'
    internal = 'metadata/package/description/visibility::nupkg-description-internal-term'
    process_ref = 'metadata/binary/symbols/name/process::dotnet-process-start-import'
    directory_ref = 'micro-behaviors/fs/delete/directory::dotnet-directory-delete-import'
    focus = {process, directory, process_ref, directory_ref, internal}
    sample = next(args.samples_root.rglob('Systemm.Drawing.Common.1.0.4.nupkg'))
    with zipfile.ZipFile(sample) as archive:
        original = archive.read('tasks/Systemm.Drawing.Common.Tasks.dll')
    with tempfile.TemporaryDirectory(prefix='nuget-task-capabilities-') as temporary:
        work = Path(temporary)
        cases = {
            'task.dll': (original, {process, directory, process_ref, directory_ref}),
            'renamed-package.dll': (original.replace(b'Systemm.Drawing.Common', b'Example.Drawing.Common'), {process, directory, process_ref, directory_ref}),
            'no-process-start.dll': (original.replace(b'Start', b'Starp'), {directory, directory_ref}),
            'no-directory-delete.dll': (original.replace(b'Directory', b'Directorz'), {process, process_ref}),
        }
        for name, (content, _) in cases.items():
            (work / name).write_bytes(content)
        for name, description, required in [
            ('review.nupkg', 'An internal security review', {internal}),
            ('private.nupkg', 'An intranet package', {internal}),
            ('public.nupkg', 'A public library', set()),
        ]:
            with zipfile.ZipFile(work / name, 'w') as archive:
                archive.writestr('Example.nuspec', '<package><metadata><id>Example</id><version>1.0</version><description>' + description + '</description></metadata></package>')
            cases[name] = (b'', required)
        credentials = 'micro-behaviors/os/security/auth/password::postgres-default-credential-literal'
        focus.add(credentials)
        for name, body, expected in [
            ('default-credentials.cs', 'string value = "Host=localhost;Username=postgres;Password=postgres";', {credentials}),
            ('default-credentials-spaces.cs', 'string value = "Username = postgres ; Password = postgres";', {credentials}),
            ('credential-comment.cs', '// Username=postgres;Password=postgres', set()),
            ('empty-password.cs', 'string value = "Username=postgres;Password=";', set()),
            ('nondefault-password.cs', 'string value = "Username=postgres;Password=postgres-other";', set()),
        ]:
            (work / name).write_text('class Configuration { ' + body + '\n}')
            cases[name] = (b'', expected)
        # The word inside an unrelated XML description is not NuGet identity.
        (work / 'unrelated.xml').write_text('<Report><description>internal review</description></Report>')
        cases['unrelated.xml'] = (b'', set())
        deception = 'objectives/supply-chain/impersonation/package/manifest::nuget-drawing-claim-build-cleanup'
        focus.add(deception)
        for name, honest, runtime, expected in [
            ('disguised.nupkg', False, False, {process_ref, directory_ref, deception, credentials}),
            ('declared-cleanup.nupkg', True, False, {process_ref, directory_ref, credentials}),
            ('with-runtime-library.nupkg', False, True, {process_ref, directory_ref, credentials}),
        ]:
            with zipfile.ZipFile(sample) as archive, zipfile.ZipFile(work / name, 'w') as output:
                for member in archive.namelist():
                    content = archive.read(member)
                    if honest and member.endswith('.nuspec'):
                        content = content.replace(b'Provides access to GDI+ bitmap drawing APIs for .NET applications.', b'Project scaffolding and dependency cleanup tasks.')
                    output.writestr(member, content)
                if runtime:
                    output.writestr('lib/net10.0/Example.dll', original)
            cases[name] = (b'', expected)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)], check=True, capture_output=True, text=True)
        seen = set()
        for line in result.stdout.strip().split('\n'):
            file = json.loads(line)['files'][0]
            name = Path(file['path']).name
            actual = {t['id'] for t in file.get('traits', [])} & focus
            if name.endswith('.nupkg'):
                actual -= {process, directory}
            assert actual == cases[name][1], (name, actual, cases[name][1])
            seen.add(name)
        assert seen == cases.keys()
    print(f'NuGet build-task improve controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
