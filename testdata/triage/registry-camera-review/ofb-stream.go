package cryptoexample
import "crypto/cipher"
func transform(block cipher.Block, iv, output, input []byte) {
 stream := cipher.NewOFB(block, iv)
 stream.XORKeyStream(output, input)
}
