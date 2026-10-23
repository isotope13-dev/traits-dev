package sample
import "crypto/cipher"
func decrypt(block cipher.Block, nonce, ciphertext []byte) []byte {
    aead, _ := cipher.NewGCM(block)
    plain, _ := aead.Open(nil, nonce, ciphertext, nil)
    return plain
}
