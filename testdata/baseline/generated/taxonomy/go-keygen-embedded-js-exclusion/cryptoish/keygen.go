//go:build keygen

package cryptoish

type KeyHolder struct {
	seed byte
}

//go:noinline
func (k *KeyHolder) GenerateKey() [32]byte {
	var key [32]byte
	for i := range key {
		key[i] = k.seed + byte(i)
	}
	return key
}
