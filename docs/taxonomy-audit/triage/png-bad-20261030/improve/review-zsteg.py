"""Normalize zsteg output and select candidates for full-stream extraction."""
import ast
import collections
import json
from pathlib import Path
import re
import warnings

warnings.filterwarnings('ignore', category=SyntaxWarning)
work=Path('/tmp/png-bad-improve/zsteg')
paths=json.loads(Path('/tmp/png-bad-triage/paths.json').read_text())
rows=[];selected=[];texts=[];types=collections.Counter()
for file in sorted(work.glob('*.stdout')):
    for line in file.read_text(errors='replace').splitlines():
        m=re.match(r'^\s*(.*?)\s*\.\. (.+)',line)
        if not m:continue
        row=dict(index=int(file.stem),method=m[1].strip(),result=m[2])
        rows.append(row)
        if m[2].startswith('file:'):types[m[2].split(',')[0]]+=1
        interesting=any(v in m[2] for v in ['wbStego','OpenStego','Camouflage','zlib:'])
        if m[2].startswith('file:') and re.search(r'(?i)executable|compressed|archive|script',m[2]):interesting=True
        if m[2].startswith('text: '):
            try:
                s=ast.literal_eval(m[2][6:])
                if len(set(s))>=12 and (re.search(r'[A-Za-z]{4,}[ \t]+[A-Za-z]{4,}',s) or re.search(r'(?i)<\?php|powershell|https?://|eval\(|/bin/sh',s)):
                    texts.append(row);interesting=True
            except (ValueError,SyntaxError):pass
        if interesting:
            row={**row,'path':paths[row['index']-1]}
            selected.append(row)
(work/'candidates.json').write_text(json.dumps(rows,indent=2)+'\n')
(work/'selected.json').write_text(json.dumps(selected,indent=2)+'\n')
(work/'text-review.json').write_text(json.dumps(texts,indent=2)+'\n')
(work/'file-type-counts.json').write_text(json.dumps(types,indent=2)+'\n')
print(len(list(work.glob('*.stdout'))),'outputs;',len(rows),'results;',len(selected),'selected for validation')
