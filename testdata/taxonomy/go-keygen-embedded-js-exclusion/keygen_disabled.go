//go:build !keygen

package main

func runKeyGeneration() [32]byte {
	return [32]byte{1}
}
