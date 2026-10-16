//go:build keygen

package main

import "example.test/keygenprobe/cryptoish"

func runKeyGeneration() [32]byte {
	return new(cryptoish.KeyHolder).GenerateKey()
}
