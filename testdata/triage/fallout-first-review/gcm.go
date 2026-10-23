package sample
import c "crypto/cipher"
func encrypt(block c.Block, nonce, plain []byte) []byte {
    aead, _ := c.NewGCM(block)
    return aead.Seal(nil, nonce, plain, nil)
}
