package main

import (
 "bytes"
 "encoding/json"
 "fmt"
 "image"
 "image/color"
 "image/draw"
 "image/png"
 "os"
 "path/filepath"
 "regexp"
)

var digits = []string{"111101101101111", "010110010010111", "111001111100111", "111001111001111", "101101111001001", "111100111001111", "111100111101111", "111001001001001", "111101111101111", "111101111001111"}
func label(dst *image.NRGBA, n, x, y int) {
 for _, ch := range fmt.Sprintf("%03d", n) {
  for i, b := range digits[ch-'0'] { if b=='1' { draw.Draw(dst,image.Rect(x+i%3*2,y+i/3*2,x+i%3*2+2,y+i/3*2+2), &image.Uniform{color.NRGBA{0,0,0,255}},image.Point{},draw.Src) } }; x+=8
 }
}
func main() {
 data,err:=os.ReadFile("/tmp/png-bad-triage/paths.json"); if err!=nil { panic(err) }; var paths []string; json.Unmarshal(data,&paths)
 sheets:=[]*image.NRGBA{}
 for i:=0;i<4;i++ { s:=image.NewNRGBA(image.Rect(0,0,1000,1000)); draw.Draw(s,s.Bounds(),&image.Uniform{color.NRGBA{235,235,235,255}},image.Point{},draw.Src); sheets=append(sheets,s) }
 code:=regexp.MustCompile(`(?i)<\?php|<script|powershell|frombase64string|/bin/(sh|bash)|cmd\.exe|eval\(|exec\(|https?://[^\s\x00]{12,}`)
 findings:=[]map[string]any{}
 for idx,path:=range paths {
  f,e:=os.Open(path);if e!=nil {panic(e)}; im,e:=png.Decode(f); f.Close();if e!=nil{panic(e)}
  b:=im.Bounds(); w,h:=b.Dx(),b.Dy(); scale:=min(180.0/float64(w),170.0/float64(h)); nw,nh:=int(float64(w)*scale),int(float64(h)*scale)
  cell:=idx%25; x,y:=(cell%5)*200,(cell/5)*200; dst:=sheets[idx/25];label(dst,idx+1,x+5,y+5)
  for yy:=0;yy<nh;yy++ {for xx:=0;xx<nw;xx++ { c:=color.NRGBAModel.Convert(im.At(b.Min.X+xx*w/nw,b.Min.Y+yy*h/nh)).(color.NRGBA); bg:=uint8(190);if ((xx/8)+(yy/8))%2==0{bg=225};a:=uint32(c.A);dst.SetNRGBA(x+10+xx,y+20+yy,color.NRGBA{uint8((uint32(c.R)*a+uint32(bg)*(255-a))/255),uint8((uint32(c.G)*a+uint32(bg)*(255-a))/255),uint8((uint32(c.B)*a+uint32(bg)*(255-a))/255),255}) }}
  pixels:=make([]color.NRGBA,0,w*h); invisible:=[]byte{}
  for yy:=b.Min.Y;yy<b.Max.Y;yy++ {for xx:=b.Min.X;xx<b.Max.X;xx++ {c:=color.NRGBAModel.Convert(im.At(xx,yy)).(color.NRGBA); pixels=append(pixels,c);if c.A==0 {invisible=append(invisible,c.R,c.G,c.B)}}}
  streams:=0
  raw:=make([]byte,0,len(pixels)*4); for _,p:=range pixels {raw=append(raw,p.R,p.G,p.B,p.A)};os.MkdirAll("/tmp/png-bad-triage/decoded",0755);os.WriteFile(fmt.Sprintf("/tmp/png-bad-triage/decoded/%03d.rgba",idx+1),raw,0644)
  for _,order:=range []string{"r","g","b","a","rgb","bgr","rgba","abgr"} { for bit:=0;bit<2;bit++ { for endian:=0;endian<2;endian++ {
   out:=make([]byte,0,len(pixels)*len(order)/8);var cur byte;var used uint
   for _,p:=range pixels {for _,ch:=range order {v:=p.R;switch ch{case 'g':v=p.G;case 'b':v=p.B;case 'a':v=p.A}; v=(v>>bit)&1;if endian==0 {cur=(cur<<1)|v}else{cur|=v<<used};used++;if used==8{out=append(out,cur);cur=0;used=0}}}
   streams++
   if m:=code.FindAll(out,-1);len(m)>0 { vals:=[]string{};for _,v:=range m{vals=append(vals,string(v))};findings=append(findings,map[string]any{"index":idx+1,"path":path,"order":order,"bit":bit,"endian":endian,"code":vals}) }
   // Reject accidental two-byte MZ matches unless the referenced PE header is valid.
   for pos:=0;pos+64<len(out);pos++ {if out[pos]!='M'||out[pos+1]!='Z'{continue};q:=out[pos+60:];off:=int(q[0])|int(q[1])<<8|int(q[2])<<16|int(q[3])<<24;if off>=64&&off<len(out)-pos-4&&bytes.Equal(out[pos+off:pos+off+4],[]byte{'P','E',0,0}){findings=append(findings,map[string]any{"index":idx+1,"kind":"PE","order":order,"bit":bit,"endian":endian,"offset":pos})}}
   for _,magic:=range [][]byte{{0x7f,'E','L','F'},{'P','K',3,4},{0x1f,0x8b,8}}{if pos:=bytes.Index(out,magic);pos>=0 {findings=append(findings,map[string]any{"index":idx+1,"kind":"magic candidate","magic":fmt.Sprintf("%x",magic),"order":order,"bit":bit,"endian":endian,"offset":pos});os.WriteFile(fmt.Sprintf("/tmp/png-bad-triage/decoded/candidate-%03d-%s-%d-%d.bin",idx+1,order,bit,endian),out[pos:],0644)}}
  }}}
  if m:=code.FindAll(invisible,-1);len(m)>0 { findings=append(findings,map[string]any{"index":idx+1,"kind":"invisible RGB code","matches":fmt.Sprintf("%q",m)}) }
  fmt.Printf("%03d %s %dx%d %s streams=%d\n",idx+1,filepath.Base(path),w,h,path,streams)
 }
 for idx,s:=range sheets {f,e:=os.Create(fmt.Sprintf("/tmp/png-bad-triage/contact-%d.png",idx+1));if e!=nil{panic(e)};png.Encode(f,s);f.Close()}
 data,_=json.MarshalIndent(findings,"","  ");os.WriteFile("/tmp/png-bad-triage/pixel-candidates.json",data,0644)
}
