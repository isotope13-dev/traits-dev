package signing
import ("crypto/ed25519"; "crypto/sha512")
func sign(key ed25519.PrivateKey, msg []byte) []byte {
    return ed25519.Sign(key, msg)
}
func prefix(secret []byte) [64]byte {
    return sha512.Sum512([]byte("Derive temporary signing key hash input" + string(secret)))
}
