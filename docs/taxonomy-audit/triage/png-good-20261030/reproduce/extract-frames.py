"""Reframe APNG compressed sample data without compositing or losing transparent RGB."""
from pathlib import Path
import hashlib
import json
import struct
import zlib

work = Path('/tmp/png-good-triage')
images = Path('/home/t/src/traits-dev/.triage-work/png-good/pngs')
out = Path('/home/t/src/traits-dev/.triage-work/png-good/frames')
out.mkdir(exist_ok=True)
records = []
limits = []

def chunk(kind, body):
    return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)

with (work / 'layouts.jsonl').open() as f:
    animations = [json.loads(line) for line in f if 'acTL' in json.loads(line)['chunks']]
for item in animations:
    source = item['sha256']
    data = (images / (source + '.png')).read_bytes()
    pos = 8
    ancillary = []
    header = None
    frames = []
    current = None
    while pos + 12 <= len(data):
        size, kind = struct.unpack_from('>I4s', data, pos)
        body = data[pos + 8:pos + 8 + size]
        pos += size + 12
        if kind == b'IHDR': header = body
        elif kind in [b'PLTE', b'tRNS']: ancillary.append((kind, body))
        elif kind == b'fcTL' and len(body) == 26:
            if len(frames) >= 1024:
                limits.append({'source': source, 'reason': 'more than 1024 frames'})
                break
            width, height = struct.unpack_from('>II', body, 4)
            current = {'width': width, 'height': height, 'data': bytearray()}
            frames.append(current)
        elif kind == b'IDAT' and current is not None: current['data'].extend(body)
        elif kind == b'fdAT' and current is not None: current['data'].extend(body[4:])
        elif kind == b'IEND': break
    for index, frame in enumerate(frames):
        if not header or not frame['data']: continue
        encoded = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>II', frame['width'], frame['height']) + header[8:])
        encoded += b''.join(chunk(kind, body) for kind, body in ancillary)
        encoded += chunk(b'IDAT', frame['data']) + chunk(b'IEND', b'')
        sha = hashlib.sha256(encoded).hexdigest()
        dest = out / (sha + '.png')
        if not dest.exists(): dest.write_bytes(encoded)
        records.append({'source_sha256': source, 'frame': index, 'sha256': sha, 'path': str(dest)})
(work / 'frames.json').write_text(json.dumps({'animations': len(animations), 'frames': records, 'limits': limits}, indent=2) + '\n')
print('Animations', len(animations), 'frames', len(records), 'unique', len({r['sha256'] for r in records}), 'limits', limits)
