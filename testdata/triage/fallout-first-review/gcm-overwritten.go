package sample
import "crypto/cipher"
type Envelope struct{}
func (e Envelope) Seal() {}
func unrelated(block cipher.Block, envelope Envelope) {
    aead, _ := cipher.NewGCM(block)
    aead = envelope
    aead.Seal()
}
