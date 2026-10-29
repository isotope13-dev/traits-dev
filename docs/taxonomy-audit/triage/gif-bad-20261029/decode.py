import ctypes as C,ctypes.util,json,zlib,struct,hashlib
from pathlib import Path
class Color(C.Structure):_fields_=[('r',C.c_ubyte),('g',C.c_ubyte),('b',C.c_ubyte)]
class Palette(C.Structure):_fields_=[('count',C.c_int),('bits',C.c_int),('sorted',C.c_bool),('colors',C.POINTER(Color))]
class Desc(C.Structure):_fields_=[('left',C.c_int),('top',C.c_int),('width',C.c_int),('height',C.c_int),('interlace',C.c_bool),('palette',C.POINTER(Palette))]
class Ext(C.Structure):_fields_=[('count',C.c_int),('bytes',C.POINTER(C.c_ubyte)),('function',C.c_int)]
class Frame(C.Structure):_fields_=[('desc',Desc),('pixels',C.POINTER(C.c_ubyte)),('ext_count',C.c_int),('ext',C.POINTER(Ext))]
class GIF(C.Structure):_fields_=[('width',C.c_int),('height',C.c_int),('resolution',C.c_int),('background',C.c_int),('aspect',C.c_ubyte),('palette',C.POINTER(Palette)),('count',C.c_int),('image',Desc),('frames',C.POINTER(Frame)),('ext_count',C.c_int),('ext',C.POINTER(Ext)),('error',C.c_int),('user',C.c_void_p),('private',C.c_void_p)]
class GCB(C.Structure):_fields_=[('disposal',C.c_int),('input',C.c_bool),('delay',C.c_int),('transparent',C.c_int)]
lib=C.CDLL(ctypes.util.find_library('gif'));lib.DGifOpenFileName.argtypes=[C.c_char_p,C.POINTER(C.c_int)];lib.DGifOpenFileName.restype=C.POINTER(GIF);lib.DGifSlurp.argtypes=[C.POINTER(GIF)];lib.DGifCloseFile.argtypes=[C.POINTER(GIF),C.POINTER(C.c_int)];lib.DGifSavedExtensionToGCB.argtypes=[C.POINTER(GIF),C.c_int,C.POINTER(GCB)]
def png(path,w,h,rgb):
 def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
 raw=b''.join(b'\0'+rgb[y*w*3:(y+1)*w*3] for y in range(h))
 Path(path).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
def sheet(path,images,cols,cellw,cellh):
 rows=(len(images)+cols-1)//cols;w=cols*cellw;h=rows*cellh;out=bytearray(b'\xdd\xdd\xdd'*(w*h))
 for i,(iw,ih,rgb) in enumerate(images):
  scale=min((cellw-8)/iw,(cellh-8)/ih,4);dw=max(1,int(iw*scale));dh=max(1,int(ih*scale));ox=(i%cols)*cellw+(cellw-dw)//2;oy=(i//cols)*cellh+(cellh-dh)//2
  for y in range(dh):
   for x in range(dw):
    src=(min(ih-1,int(y/scale))*iw+min(iw-1,int(x/scale)))*3;dst=((oy+y)*w+ox+x)*3;out[dst:dst+3]=rgb[src:src+3]
 png(path,w,h,out)
rows=json.loads(Path('/tmp/gif-bad-triage/structure.json').read_text());icons=[];index=[];checks=[]
for row in rows:
 err=C.c_int();ptr=lib.DGifOpenFileName(row['path'].encode(),C.byref(err));assert ptr,(row['path'],err.value)
 try:
  assert lib.DGifSlurp(ptr)==1,(row['path'],ptr.contents.error)
  g=ptr.contents;assert g.count==len(row['structure']['frames']);assert g.width*g.height<2_000_000
  canvas=bytearray(b'\x44\x44\x44'*(g.width*g.height));images=[];pixel_checks=[]
  for i in range(g.count):
   f=g.frames[i];d=f.desc;pal=d.palette.contents if d.palette else g.palette.contents;pixels=C.string_at(f.pixels,d.width*d.height)
   assert max(pixels)<pal.count,(row['path'],i,'palette');assert d.left+d.width<=g.width and d.top+d.height<=g.height
   own=row['structure']['frames'][i]
   if not d.interlace:assert hashlib.sha256(pixels).hexdigest()==own['pixel_sha256']
   else:
    encoded=b''.join(pixels[y*d.width:(y+1)*d.width] for start,step in [(0,8),(4,8),(2,4),(1,2)] for y in range(start,d.height,step));assert hashlib.sha256(encoded).hexdigest()==own['pixel_sha256']
   ctl=GCB();ctl.transparent=-1;lib.DGifSavedExtensionToGCB(ptr,i,C.byref(ctl));previous=canvas[:]
   for y in range(d.height):
    for x in range(d.width):
     value=pixels[y*d.width+x]
     if value!=ctl.transparent:
      color=pal.colors[value];off=((d.top+y)*g.width+d.left+x)*3;canvas[off:off+3]=bytes((color.r,color.g,color.b))
   images.append((g.width,g.height,bytes(canvas)))
   if ctl.disposal==2:
    for y in range(d.height):
     off=((d.top+y)*g.width+d.left)*3;canvas[off:off+d.width*3]=b'\x44\x44\x44'*d.width
   elif ctl.disposal==3:canvas=previous
  checks.append({'sha256':row['sha256'],'frames':g.count,'giflib_decode':'pass','all_palettes_valid':True,'all_rectangles_in_canvas':True,'independent_pixel_hashes_match':True})
  if g.count>1:sheet('/tmp/gif-bad-triage/'+row['sha256'][:12]+'-frames.png',images,10 if g.count>10 else 4,96 if g.count>10 else 300,96 if g.count>10 else 180)
  icons.append(images[0]);index.append({'cell':len(icons)-1,'sha256':row['sha256'],'name':Path(row['path']).name})
 finally:lib.DGifCloseFile(ptr,C.byref(err))
sheet('/tmp/gif-bad-triage/contact-sheet.png',icons,10,96,96)
Path('/tmp/gif-bad-triage/independent-decode.json').write_text(json.dumps(checks,indent=2));Path('/tmp/gif-bad-triage/contact-sheet-index.json').write_text(json.dumps(index,indent=2))
print('Independent giflib validation passed',len(checks),'files',sum(x['frames'] for x in checks),'frames; all pixel hashes match')
