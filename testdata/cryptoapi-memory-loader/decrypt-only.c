#include <windows.h>
#include <wincrypt.h>
int decrypt(HCRYPTPROV p, BYTE *blob, DWORD n, BYTE *buf, DWORD *len) { HCRYPTKEY key; if (!CryptImportKey(p,blob,n,0,0,&key)) return 0; return CryptDecrypt(key,0,TRUE,0,buf,len); }
