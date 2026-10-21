#include <windows.h>
#include <wincrypt.h>
BOOL add(const BYTE *der, DWORD len) {
 HCERTSTORE store = CertOpenSystemStoreA(0, "MY");
 return CertAddEncodedCertificateToStore(store, X509_ASN_ENCODING, der, len, 1, NULL);
}
