package main
import "crypto/rand"
func randomBytes(b []byte) { rand.Read(b) }
