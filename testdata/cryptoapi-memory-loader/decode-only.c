#include <windows.h>
#include <wincrypt.h>
int decode(const char *text, BYTE *out, DWORD *size) { return CryptStringToBinaryA(text,0,CRYPT_STRING_BASE64,out,size,0,0); }
