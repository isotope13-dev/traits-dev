int checksum(unsigned char *in, int n){int b=0;for(int i=0;i<n;i++){b ^= in[i];}return b;}
