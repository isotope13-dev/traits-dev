#!/usr/bin/env python3
"""Check library markers after retiring their duplicate namespaces."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='library-marker-') as tmp:
    root = Path(tmp)
    cases = {
        'axios.js': 'class AxiosError extends Error {}\nconst version = "[Axios v1.2]";\n',
        'babel/package.json': '{"name":"@babel/cli","version":"1.0.0"}\n',
        'relative.js': 'const transform = require("../transformation");\n',
        'generic.css': '.container-xxl { color: red } .was-validated { display: block }\n',
        'named.css': '/*# sourceMappingURL=bootstrap.min.css.map */\n',
        'generic.svg': '<svg><font id="different_font"><font-face units-per-em="1200" ascent="960" descent="-240"/></font></svg>' + ' ' * 220,
        'glyphicons.svg': '<svg><font id="glyphicons_halflingsregular"><font-face units-per-em="1200" ascent="960" descent="-240"/></font></svg>' + ' ' * 220,
        'generic.scss': '$grid-breakpoints: ();\n@import "functions";\n@import "utilities/align";\n@import "utilities/position";\n',
        'other.js': 'class OtherError extends Error {}\n',
        'query.js': 'import jsonata from "jsonata";\njsonata("name").evaluate(data);\n',
    }
    for name, content in cases.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    metrics = 'micro-behaviors/ui/graphics/font::svg-font-1200-960-negative240-metrics'
    glyph_name = 'well-known/lib/ui/bootstrap::glyphicons-halflings-font-id'
    assert metrics in ids['generic.svg'], ids['generic.svg']
    assert glyph_name not in ids['generic.svg']
    assert metrics in ids['glyphicons.svg'] and glyph_name in ids['glyphicons.svg'], ids['glyphicons.svg']
    css = 'micro-behaviors/ui/window/style::css-responsive-utility-class-text'
    bootstrap = 'well-known/lib/ui/bootstrap::bootstrap-css-source-map'
    sass = 'metadata/import/framework::sass-core-and-layout-utility-imports'
    assert css in ids['generic.css'], ids['generic.css']
    assert bootstrap not in ids['generic.css']
    assert bootstrap in ids['named.css'], ids['named.css']
    assert sass in ids['generic.scss'], ids['generic.scss']
    babel = 'well-known/lib/development/babel-toolchain/babel::babel-cli-package'
    relative = 'metadata/import/module::relative-transformation-require-text'
    assert babel in ids['package.json'], ids['package.json']
    assert relative in ids['relative.js'], ids['relative.js']
    assert babel not in ids['relative.js']
    axios_class = 'well-known/lib/network/axios::axios-class'
    axios_version = 'well-known/lib/network/axios::axios-version'
    query = 'well-known/lib/data/jsonata::jsonata-evaluate-call'
    assert {axios_class, axios_version} <= ids['axios.js'], ids['axios.js']
    assert axios_class not in ids['other.js'] and axios_version not in ids['other.js']
    assert query in ids['query.js'], ids['query.js']
    assert not any('-legacy::' in t for group in ids.values() for t in group)
    print('Product identities and generic import observations remain distinct.')
