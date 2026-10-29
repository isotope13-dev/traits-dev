package nonce
import "encoding/hex"
func prefix() ([]byte, error) {
    return hex.DecodeString("0b4f49847218185bcde63c568cc8897ae21ad33809c8e7d0e6401ea7d6a4019f")
}
