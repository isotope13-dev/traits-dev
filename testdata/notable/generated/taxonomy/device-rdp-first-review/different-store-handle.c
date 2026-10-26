#include <windows.h>
#include <wincrypt.h>
BOOL add(HCERTSTORE other, const BYTE *der, DWORD len) {
 HCERTSTORE root = CertOpenSystemStoreA(0, "ROOT");
 return CertAddEncodedCertificateToStore(other, X509_ASN_ENCODING, der, len, 1, NULL);
}
