package main
import (
 "crypto/rand"
 "crypto/rsa"
 "crypto/sha256"
 "fmt"
 "time"
)
type session struct { stop bool }

//go:noinline
func (s *session) tcpStreamScreen() {
 for !s.stop { time.Sleep(time.Millisecond) }
}

func main() {
 go (&session{}).tcpStreamScreen()
 key, err := rsa.GenerateKey(rand.Reader, 2048)
 if err != nil { panic(err) }
 ciphertext, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, &key.PublicKey, []byte("test"), nil)
 fmt.Println("exodus.wallet", len(ciphertext), err)
}
