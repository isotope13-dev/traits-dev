package nonce
import "crypto/sha512"
func prefix() [64]byte {
    return sha512.Sum512([]byte("Derive temporary signing key hash input"))
}
