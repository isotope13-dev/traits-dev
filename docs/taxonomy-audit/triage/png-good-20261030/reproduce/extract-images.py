"""Stream package members, retaining content-addressed PNGs without extracting paths."""
from pathlib import Path
import hashlib
import gzip
import io
import json
import tarfile
import zipfile
import subprocess

WORK = Path('/tmp/png-good-triage')
OUT = Path('/home/t/src/traits-dev/.triage-work/png-good/pngs')
OUT.mkdir(parents=True, exist_ok=True)
checkpoint = json.loads((WORK / "extracted-images.json").read_text()) if (WORK / "extracted-images.json").exists() else {}
images = checkpoint.get("images", [])
archives = checkpoint.get("archives", [])
limits = checkpoint.get("limits", [])
done = {row["path"] for row in archives if "!!" not in row["path"] and row["error"] is None}
done.update(row["source"] for row in images if row["member"] == "")
MAX = 64 * 1024 * 1024

def member(source, name, stream, size, depth):
    head = stream.read(16)
    if head.startswith(b'\x89PNG\r\n\x1a\n'):
        if size > MAX:
            limits.append({'path': source + '!!' + name, 'reason': 'PNG exceeds 64 MiB'})
            return
        data = head + stream.read(MAX + 1)
        if len(data) > MAX:
            limits.append({'path': source + '!!' + name, 'reason': 'PNG exceeds 64 MiB'})
            return
        sha = hashlib.sha256(data).hexdigest()
        p = OUT / (sha + '.png')
        if not p.exists(): p.write_bytes(data)
        images.append({'source': source, 'member': name, 'sha256': sha, 'size': len(data), 'path': str(p)})
    elif depth < 2 and name.lower().endswith(('.tar.gz', '.tgz', '.tar.xz', '.tar.bz2', '.zip', '.jar')):
        if size > MAX:
            limits.append({'path': source + '!!' + name, 'reason': 'nested archive exceeds 64 MiB; primary scanner handles it'})
            return
        data = head + stream.read(MAX + 1)
        if len(data) <= MAX:
            archive(io.BytesIO(data), source + '!!' + name, depth + 1)

def archive(handle, source, depth=0, tar_only=False):
    count = 0
    before = len(images)
    try:
        if not tar_only and (not hasattr(handle, "seekable") or handle.seekable()) and zipfile.is_zipfile(handle):
            with zipfile.ZipFile(handle) as z:
                for entry in z.infolist():
                    if entry.is_dir(): continue
                    count += 1
                    with z.open(entry) as stream:
                        member(source, entry.filename, stream, entry.file_size, depth)
        else:
            if hasattr(handle, 'seekable') and handle.seekable(): handle.seek(0)
            with tarfile.open(fileobj=handle if hasattr(handle, 'read') else None,
                              name=None if hasattr(handle, 'read') else handle,
                              mode='r|*', ignore_zeros=True) as z:
                for entry in z:
                    if not entry.isfile(): continue
                    count += 1
                    member(source, entry.name, z.extractfile(entry), entry.size, depth)
        archives.append({'path': source, 'entries': count, 'pngs': len(images) - before, 'error': None})
    except Exception as exc:
        archives.append({'path': source, 'entries': count, 'pngs': len(images) - before, 'error': str(exc)})

for row in json.loads((WORK / 'inventory.json').read_text()):
    if row['path'] in done: continue
    if row['magic'].startswith('89504e470d0a1a0a'):
        with open(row['path'], 'rb') as f: member(row['path'], '', f, row['size'], 0)
    elif row['path'].endswith('.rpm'):
        # libarchive lists the source RPM; its source tarball is then streamed
        # through stdout, avoiding filesystem extraction of archive paths.
        listing = subprocess.run(['bsdtar', '-tf', row['path']], capture_output=True, text=True, check=True).stdout.splitlines()
        for name in listing:
            if name.endswith(('.tar.gz', '.tar.xz', '.tar.bz2', '.tgz')):
                proc = subprocess.Popen(['bsdtar', '-xOf', row['path'], name], stdout=subprocess.PIPE)
                archive(proc.stdout, row['path'] + '!!' + name, 1)
                proc.stdout.close()
                proc.wait()
    elif row['path'].endswith('.apk'):
        # APK v2 has concatenated gzip members. gzip.GzipFile consumes every
        # member; tarfile's streaming gzip decoder handles only the first.
        with gzip.open(row['path'], 'rb') as stream:
            archive(stream, row['path'], tar_only=True)
    elif not row['magic'].startswith('4d4d002a'):
        archive(row['path'], row['path'])
    report = {'images': images, 'archives': archives, 'limits': limits}
    (WORK / 'extracted-images.json').write_text(json.dumps(report, indent=2) + '\n')
    print(row['sha256'][:12], 'images', len(images), 'archives', len(archives), flush=True)
print('COMPLETE', len(images), 'image occurrences;', len({x['sha256'] for x in images}), 'unique PNGs', flush=True)
