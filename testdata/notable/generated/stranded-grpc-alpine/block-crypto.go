package aes
func transform(out, in []byte) {
 encryptBlock(key, out, in)
 decryptBlockGeneric(key, out, in)
}
