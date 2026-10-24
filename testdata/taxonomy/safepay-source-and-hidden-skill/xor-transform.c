void transform(unsigned char *in, unsigned char *out, int n, int key){for(int i=0;i<n;i++){unsigned char b=in[i];b ^= key;out[i]=(char)b;}}
