package main
import (
 "crypto/aes"
 "crypto/cipher"
 "crypto/tls"
 "fmt"
 "net/http"
)
func main() {
 block, _ := aes.NewCipher(make([]byte, 16))
 _ = cipher.NewCBCEncrypter(block, make([]byte, 16))
 fmt.Printf("%T %T %T\n", http.DefaultClient, tls.Client, block)
}
