import collections
import ctypes as c
import hashlib
import json
from pathlib import Path
import struct
import zlib
from PIL import Image, ImageDraw

WORK = Path('/tmp/png-good-triage')
rows = []
images = []
for item in json.loads((WORK / 'inventory.json').read_text()):
    p = Path(item['path'])
    data = p.read_bytes() if item['magic'].startswith('89504e47') or p.suffix == '.png' else None
    if data is None:
        continue
    row = {**item, 'chunks': [], 'errors': [], 'texts': []}
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        pos = 8
        idat = bytearray()
        while pos + 12 <= len(data):
            size, kind = struct.unpack_from('>I4s', data, pos)
            end = pos + 12 + size
            if end > len(data):
                row['errors'].append('truncated chunk')
                break
            body = data[pos + 8:end - 4]
            crc = struct.unpack_from('>I', data, end - 4)[0]
            crc_ok = zlib.crc32(kind + body) & 0xffffffff == crc
            row['chunks'].append({'kind': kind.decode('ascii', errors='replace'), 'size': size, 'crc_ok': crc_ok})
            if not crc_ok:
                row['errors'].append('bad CRC: ' + repr(kind))
            if kind == b'IHDR':
                row['ihdr'] = list(struct.unpack('>IIBBBBB', body))
            if kind == b'IDAT':
                idat.extend(body)
            if kind in [b'tEXt', b'iTXt', b'zTXt']:
                row['texts'].append({'kind': kind.decode(), 'preview': body[:4096].decode('utf-8', errors='replace'), 'size': size})
            pos = end
            if kind == b'IEND':
                break
        row['trailing_bytes'] = len(data) - pos
        row['trailing_preview'] = data[pos:pos + 128].hex()
        try:
            dec = zlib.decompressobj()
            expanded = dec.decompress(idat, 256 * 1024 * 1024)
            row['idat'] = {'compressed': len(idat), 'decompressed': len(expanded), 'eof': dec.eof, 'unused': len(dec.unused_data), 'unconsumed': len(dec.unconsumed_tail)}
            if dec.unused_data:
                row['unused_idat_preview'] = dec.unused_data[:128].hex()
        except zlib.error as exc:
            row['errors'].append(str(exc))
    try:
        with Image.open(p) as image:
            row['pillow'] = {'format': image.format, 'mode': image.mode, 'dimensions': image.size, 'frames': getattr(image, 'n_frames', 1)}
            image.load()
            thumb = image.convert('RGBA')
            thumb.thumbnail((230, 190))
            images.append((p, thumb.copy()))
    except Exception as exc:
        row['errors'].append('decode: ' + str(exc))
    rows.append(row)
(WORK / 'structure.json').write_text(json.dumps(rows, indent=2) + '\n')
for offset in range(0, len(images), 20):
    sheet = Image.new('RGB', (1250, 1000), '#dddddd')
    draw = ImageDraw.Draw(sheet)
    for cell, (path, im) in enumerate(images[offset:offset + 20]):
        x, y = cell % 5 * 250, cell // 5 * 250
        for yy in range(25, 220, 10):
            for xx in range(0, 240, 10):
                draw.rectangle((x + xx, y + yy, x + xx + 9, y + yy + 9), fill='#eeeeee' if (xx // 10 + yy // 10) % 2 else '#bdbdbd')
        sheet.paste(im, (x + 5, y + 25), im)
        draw.text((x + 4, y + 3), f'{offset + cell + 1:03d} {path.parts[5][:12]}', fill='black')
        draw.text((x + 4, y + 225), path.name[:28], fill='black')
    sheet.save(WORK / f'contact-{offset // 20 + 1}.png')
(WORK / 'contact-index.json').write_text(json.dumps([{'index': i + 1, 'path': str(p)} for i, (p, _) in enumerate(images)], indent=2) + '\n')
print(json.dumps({'images': len(rows), 'chunk_kinds': dict(collections.Counter(ch['kind'] for row in rows for ch in row['chunks'])), 'unusual': [row for row in rows if row['errors'] or row.get('trailing_bytes') or row.get('idat', {}).get('unused')]}))
