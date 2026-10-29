#include <gif_lib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int image_count;
static void preview(const char *dir,int frame,int w,int h,uint32_t *canvas) {
 char path[4096];snprintf(path,sizeof(path),"%s/frame-%05d.ppm",dir,frame);FILE *f=fopen(path,"wb");if(!f)exit(20);
 double scale=1.;if(w>320)scale=320./w;if(h*scale>240)scale=240./h;int ow=w*scale,oh=h*scale;if(ow<1)ow=1;if(oh<1)oh=1;
 fprintf(f,"P6\n%d %d\n255\n",ow,oh);for(int y=0;y<oh;y++)for(int x=0;x<ow;x++){uint32_t c=canvas[(int)(y/scale)*w+(int)(x/scale)];unsigned char rgb[3]={c>>16,c>>8,c};fwrite(rgb,1,3,f);}fclose(f);
}
int main(int argc,char **argv) {
 if(argc!=4)return 2;int error=0;GifFileType *g=DGifOpenFileName(argv[1],&error);if(!g)return 3;int expected=atoi(argv[3]);int w=g->SWidth,h=g->SHeight;
 if(w<=0||h<=0||(uint64_t)w*h>16000000)return 4;uint32_t *canvas=malloc((size_t)w*h*4),*backup=malloc((size_t)w*h*4);if(!canvas||!backup)return 5;
 for(int i=0;i<w*h;i++)canvas[i]=0x444444;int transparent=-1,disposal=0;uint64_t pixels=0;GifRecordType record;
 while(DGifGetRecordType(g,&record)==GIF_OK && record!=TERMINATE_RECORD_TYPE) {
  if(record==EXTENSION_RECORD_TYPE){int label;GifByteType *block;if(DGifGetExtension(g,&label,&block)!=GIF_OK)return 6;
   if(label==GRAPHICS_EXT_FUNC_CODE && block && block[0]==4){disposal=(block[1]>>2)&7;transparent=(block[1]&1)?block[4]:-1;}
   while(block){if(DGifGetExtensionNext(g,&block)!=GIF_OK)return 7;}
  } else if(record==IMAGE_DESC_RECORD_TYPE){if(DGifGetImageDesc(g)!=GIF_OK)return 8;GifImageDesc d=g->Image;ColorMapObject *pal=d.ColorMap?d.ColorMap:g->SColorMap;
   if(!pal||!d.Width||!d.Height||d.Left+d.Width>w||d.Top+d.Height>h)return 9;pixels+=(uint64_t)d.Width*d.Height;if(pixels>4000000000ULL||image_count>20000)return 10;
   if(disposal==3)memcpy(backup,canvas,(size_t)w*h*4);unsigned char *line=malloc(d.Width);if(!line)return 11;uint32_t colors[256];
   for(int i=0;i<pal->ColorCount;i++)colors[i]=(pal->Colors[i].Red<<16)|(pal->Colors[i].Green<<8)|pal->Colors[i].Blue;
   int starts[4]={0,4,2,1},steps[4]={8,8,4,2};int passes=d.Interlace?4:1;
   for(int pass=0;pass<passes;pass++)for(int y=d.Interlace?starts[pass]:0;y<d.Height;y+=d.Interlace?steps[pass]:1){if(DGifGetLine(g,line,d.Width)!=GIF_OK)return 12;
    uint32_t *dest=canvas+(d.Top+y)*w+d.Left;for(int x=0;x<d.Width;x++){if(line[x]>=pal->ColorCount)return 13;if(line[x]!=transparent)dest[x]=colors[line[x]];}}
   free(line);if(image_count==0||image_count==expected/2||image_count==expected-1)preview(argv[2],image_count,w,h,canvas);
   if(disposal==3)memcpy(canvas,backup,(size_t)w*h*4);else if(disposal==2)for(int y=0;y<d.Height;y++)for(int x=0;x<d.Width;x++)canvas[(d.Top+y)*w+d.Left+x]=0x444444;
   image_count++;transparent=-1;disposal=0;
  }
 }
 if(record!=TERMINATE_RECORD_TYPE || image_count!=expected)return 14;
 printf("%d %llu\n",image_count,(unsigned long long)pixels);DGifCloseFile(g,&error);free(canvas);free(backup);return 0;
}
