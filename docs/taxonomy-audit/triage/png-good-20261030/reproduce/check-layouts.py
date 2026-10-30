from pathlib import Path
import collections
import concurrent.futures
import json
import struct
import zlib

ROOT = Path('/home/t/src/traits-dev/.triage-work/png-good/pngs')
MAX_EXPANDED = 256 * 1024 * 1024

def check(path):
    data = path.read_bytes()
    row = {'sha256': path.stem, 'size': len(data), 'chunks': [], 'errors': []}
    pos = 8
    idat = bytearray()
    ended = False
    while pos + 12 <= len(data):
        n, kind = struct.unpack_from('>I4s', data, pos)
        end = pos + n + 12
        if end > len(data):
            row['errors'].append('truncated chunk')
            break
        body = data[pos + 8:end - 4]
        crc = struct.unpack_from('>I', data, end - 4)[0]
        row['chunks'].append(kind.decode('ascii', errors='replace'))
        if zlib.crc32(kind + body) & 0xffffffff != crc:
            row['errors'].append('bad CRC: ' + repr(kind))
        if kind == b'IHDR' and len(body) == 13:
            row['dimensions'] = list(struct.unpack_from('>II', body))
        if kind == b'IDAT': idat.extend(body)
        pos = end
        if kind == b'IEND':
            ended = True
            break
    row['iend'] = ended
    row['trailing_bytes'] = len(data) - pos if ended else None
    if ended and len(data) > pos:
        row['trailing_preview_hex'] = data[pos:pos + 128].hex()
        if len(data) - pos <= 65536: row['trailer_hex'] = data[pos:].hex()
    try:
        dec = zlib.decompressobj()
        output = dec.decompress(idat, MAX_EXPANDED + 1)
        row['idat_eof'] = dec.eof
        row['expanded_bytes'] = len(output)
        row['expanded_limited'] = len(output) > MAX_EXPANDED
        row['unused_idat_bytes'] = len(dec.unused_data)
        if dec.unused_data:
            row['unused_idat_preview_hex'] = dec.unused_data[:128].hex()
            if len(dec.unused_data) <= 65536: row['unused_idat_hex'] = dec.unused_data.hex()
    except zlib.error as exc:
        row['errors'].append('IDAT: ' + str(exc))
    return row

paths = sorted(ROOT.glob('*.png'))
out = Path('/tmp/png-good-triage/layouts.jsonl')
counts = collections.Counter()
with out.open('w') as f, concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for row in pool.map(check, paths):
        f.write(json.dumps(row) + '\n')
        counts['files'] += 1
        if row['errors']: counts['with_errors'] += 1
        if row['trailing_bytes']: counts['with_trailer'] += 1
        if row.get('unused_idat_bytes'): counts['with_unused_idat'] += 1
        if 'acTL' in row['chunks']: counts['animated'] += 1
print(json.dumps(counts), flush=True)
