package main

import (
    "bytes"
    "compress/gzip"
    "crypto/ecdsa"
    "crypto/elliptic"
    "crypto/rand"
    "crypto/sha512"
    "fmt"
    "io"
)

// Benign control: sign and verify a local message, then round-trip gzip data.
func main() {
    key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
    if err != nil { panic(err) }
    digest := sha512.Sum512([]byte("local integrity check"))
    signature, err := ecdsa.SignASN1(rand.Reader, key, digest[:])
    if err != nil || !ecdsa.VerifyASN1(&key.PublicKey, digest[:], signature) {
        panic("signature verification failed")
    }
    var compressed bytes.Buffer
    writer := gzip.NewWriter(&compressed)
    writer.Write([]byte("ordinary application data"))
    writer.Close()
    reader := new(gzip.Reader)
    if err := reader.Reset(&compressed); err != nil { panic(err) }
    data, err := io.ReadAll(reader)
    if err != nil { panic(err) }
    fmt.Println(string(data))
}
