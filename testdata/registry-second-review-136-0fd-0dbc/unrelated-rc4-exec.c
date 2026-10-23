#include <stdlib.h>
#include <unistd.h>
static unsigned char blob[4096] = {1, 2, 3, 4};
void arc4(unsigned char *out, size_t n) {
    unsigned char s[256], t; unsigned i, j=0;
    for(i=0;i<256;++i)s[i]=i;
    for(i=0;i<256;++i){j=(j+s[i]+(i%7))&255;t=s[i];s[i]=s[j];s[j]=t;}
    i=j=0;
    while(n--){i=(i+1)&255;j=(j+s[i])&255;t=s[i];s[i]=s[j];s[j]=t;*out++^=s[(s[i]+s[j])&255];}
}
int main(int argc, char **argv) {
    arc4(blob, sizeof(blob));
    if(argc>1) return execvp(argv[1], argv+1);
    return blob[0];
}
