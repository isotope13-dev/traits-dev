package sample
import "crypto/cipher"
type Envelope struct{}
func (e Envelope) Seal() {}
func unrelated(block cipher.Block, envelope Envelope) {
    cipher.NewGCM(block)
    envelope.Seal()
}
