#!/usr/bin/env python3
"""Exercise code-free npm packages and PostCSS helper carrier boundaries."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

NEUTRAL_WRAPPER = 'metadata/package/files/missing-entrypoint::npm-code-free-runtime-dependency-wrapper'
HELPER_DECL = 'metadata/package/dependencies/name-form::npm-scoped-postcss-motion-helper'
KNOWN_DECL = 'metadata/package/dependencies/declaration::npm-interview-postcss-helper-dependency'
CSS_DECL = 'metadata/package/dependencies/declaration::npm-animatecss-runtime-dependency'
CARRIER = 'objectives/supply-chain/trojanized/library/hidden-dep::tailwind-animatecss-scoped-postcss-carrier'
TAILWIND = 'objectives/supply-chain/trojanized/campaign::npm-interview-tailwind-scoped-postcss-loader'


def pack(path, manifest, sources=None):
    files = {'package/package.json': json.dumps(manifest)}
    files.update({'package/' + k: v for k, v in (sources or {}).items()})
    with tarfile.open(path, 'w:gz') as archive:
        for name, value in files.items():
            data = value.encode()
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    helper = '@jasperquinn/postcss-motion-helpers'
    known = {'name': 'renamed-css-adapter', 'version': '1.0.0', 'main': 'index.js',
             'dependencies': {helper: '^1.0.1', 'animate.css': '^4.1.1'}}
    def plugin(target):
        return ("const postcss = require('postcss');\n"
                "const tailwind = require('tailwindcss/plugin');\n"
                f"const helper = require('{target}');\n"
                "module.exports = options => postcss([helper(options)]);\n")
    empty = {'name': 'unreleased-adapter', 'version': '0.0.1', 'main': 'index.js',
             'files': [], 'dependencies': {'estree-walker': '^3.0.3'}}
    cases = {
        'no-code.tgz': (empty, {'README.md': 'Work in progress.\n'}, {NEUTRAL_WRAPPER}, set(), False),
        'no-code-no-doc.tgz': (empty, {}, {NEUTRAL_WRAPPER}, set(), False),
        'shipped-code.tgz': (empty, {'index.js': 'module.exports = {};\n'}, set(), {NEUTRAL_WRAPPER}, False),
        'empty-deps.tgz': ({**empty, 'dependencies': {}}, {}, set(), {NEUTRAL_WRAPPER}, False),
        'no-files-field.tgz': ({k: v for k, v in empty.items() if k != 'files'}, {}, set(), {NEUTRAL_WRAPPER}, False),
        'ordinary-scope.tgz': ({**known, 'name': 'animatecss-tailwind-example',
                                'dependencies': {'@ordinary/postcss-motion-helpers': '^1.0.0', 'animate.css': '^4.1.1'}},
                               {'index.js': plugin('@ordinary/postcss-motion-helpers')},
                               {HELPER_DECL, CSS_DECL}, {KNOWN_DECL, CARRIER, TAILWIND}, False),
        'known-loader-renamed.tgz': (known, {'index.js': plugin(helper)},
                                     {HELPER_DECL, KNOWN_DECL, CSS_DECL, CARRIER, TAILWIND}, set(), True),
        'known-array-comments.tgz': (known, {'index.js': plugin(helper).replace('postcss([helper(options)])', 'postcss(/* prepare */ [/* factory */ helper(options)])')},
                                      {KNOWN_DECL, CARRIER, TAILWIND}, set(), True),
        'known-use-comments.tgz': (known, {'index.js': plugin(helper).replace('postcss([helper(options)])', 'postcss().use(/* factory */ helper(options))')},
                                    {KNOWN_DECL, CARRIER, TAILWIND}, set(), True),
        'known-use-api-loader.tgz': (known, {'index.js': plugin(helper).replace('postcss([helper(options)])', 'postcss().use(helper(options))')},
                                      {KNOWN_DECL, CARRIER, TAILWIND, 'micro-behaviors/data/format/css::postcss-use-plugin-factory'}, set(), True),
        'known-non-postcss-use.tgz': (known, {'index.js': plugin(helper).replace('postcss([helper(options)])', 'validator().use(helper(options))')},
                                      {KNOWN_DECL}, {CARRIER, TAILWIND, 'micro-behaviors/data/format/css::postcss-plugin-factory-registration'}, False),
        'alternate-known-loader.tgz': ({**known, 'dependencies': {'@aaron205whitmore/postcss-animate-utils': '^1.0.0'}},
                                        {'index.js': plugin('@aaron205whitmore/postcss-animate-utils')},
                                        {HELPER_DECL, KNOWN_DECL, CARRIER, TAILWIND}, set(), True),
        'known-comment-only.tgz': (known, {'index.js': f'// {plugin(helper)}\nmodule.exports = {{}};\n'.replace('\n', '\n// ')},
                                    {KNOWN_DECL}, {CARRIER, TAILWIND}, False),
        'known-string-only.tgz': (known, {'index.js': f'module.exports = {json.dumps(plugin(helper))};\n'},
                                   {KNOWN_DECL}, {CARRIER, TAILWIND}, False),
        'known-executed-string.tgz': (known, {'index.js': f'module.exports = {json.dumps(plugin(helper))};\neval(module.exports);\n'},
                                       {KNOWN_DECL, CARRIER, TAILWIND}, set(), True),
        'known-unused-import.tgz': (known, {'index.js': f"const helper = require('{helper}');\nmodule.exports = helper;\n"},
                                     {KNOWN_DECL}, {CARRIER, TAILWIND}, False),
        'dev-only-helper.tgz': ({**known, 'dependencies': {'animate.css': '^4.1.1'}, 'devDependencies': {helper: '^1.0.1'}},
                                 {'index.js': plugin(helper)}, {CSS_DECL}, {HELPER_DECL, KNOWN_DECL, CARRIER, TAILWIND}, False),
    }
    with tempfile.TemporaryDirectory(prefix='npm-triage-controls-') as temporary:
        work = Path(temporary)
        for name, (manifest, sources, *_rest) in cases.items():
            pack(work / name, manifest, sources)
        result = subprocess.run([str((repo / args.cleave).resolve()), '--traits-dir', str(repo),
                                 '--format=json', str(work)], check=True, capture_output=True, text=True)
        # Binary contexts may contain Unicode NEL; only LF delimits JSONL.
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        observed = {Path(report['files'][0]['path']).name: report['files'] for report in reports}
        assert set(observed) == set(cases), ('missing archives', set(cases) - set(observed))
        for name, (_manifest, _sources, required, forbidden, hostile) in cases.items():
            files = observed[name]
            traits = [t for f in files for t in f.get('traits', [])]
            ids = {t['id'] for t in traits}
            assert required <= ids, (name, 'missing', required - ids)
            assert not (forbidden & ids), (name, 'unexpected', forbidden & ids)
            if hostile:
                directories = {t['id'].split('::')[0] for t in files[0].get('traits', []) if t['crit'] == 5}
                assert len(directories) >= 2, (name, directories)
            else:
                assert not [t['id'] for t in traits if t['crit'] >= 4], (name, 'elevated findings')
            print('PASS', name)
    print(f'{len(cases)} npm triage edge cases passed')


if __name__ == '__main__':
    main()
