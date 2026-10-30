"""Compare Go's unpremultiplied RGBA pixels with a libpng decode."""
import ctypes as c
import hashlib
import json
from pathlib import Path

class PngImage(c.Structure):
    _fields_ = [('opaque',c.c_void_p),('version',c.c_uint32),('width',c.c_uint32),
                ('height',c.c_uint32),('format',c.c_uint32),('flags',c.c_uint32),
                ('colormap_entries',c.c_uint32),('warning_or_error',c.c_uint32),
                ('message',c.c_char*64)]

lib=c.CDLL('libpng16.so.16')
lib.png_image_begin_read_from_memory.argtypes=[c.POINTER(PngImage),c.c_void_p,c.c_size_t]
lib.png_image_finish_read.argtypes=[c.POINTER(PngImage),c.c_void_p,c.c_void_p,c.c_int32,c.c_void_p]
lib.png_image_free.argtypes=[c.POINTER(PngImage)]
rows=[]
for index,path in enumerate(json.load(open('/tmp/png-bad-triage/paths.json')),1):
    data=Path(path).read_bytes();png=PngImage();png.version=1
    assert lib.png_image_begin_read_from_memory(c.byref(png),data,len(data)),(path,png.message)
    png.format=3 # PNG_FORMAT_RGB | PNG_FORMAT_FLAG_ALPHA
    out=c.create_string_buffer(png.width*png.height*4)
    assert lib.png_image_finish_read(c.byref(png),None,out,0,None),(path,png.message)
    go=Path(f'/tmp/png-bad-triage/decoded/{index:03d}.rgba').read_bytes()
    row=dict(path=path,sha256=hashlib.sha256(data).hexdigest(),width=png.width,height=png.height,
             rgba_sha256=hashlib.sha256(out.raw).hexdigest(),go_pixels_match=go==out.raw,
             libpng_diagnostic=png.message.decode(),libpng_warning_or_error=png.warning_or_error)
    rows.append(row);lib.png_image_free(c.byref(png))
Path('/tmp/png-bad-triage/independent.json').write_text(json.dumps(rows,indent=2)+'\n')
print(len(rows),'decoded;',sum(r['go_pixels_match'] for r in rows),'identical RGBA hashes')
assert all(r['go_pixels_match'] for r in rows)
