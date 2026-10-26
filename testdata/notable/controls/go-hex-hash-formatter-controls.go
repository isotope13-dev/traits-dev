package model

import "fmt"

// Fingerprint is a hash-capable metric identifier (FNV-1A 64-bit).
type Fingerprint uint64

func (f Fingerprint) String() string {
	return fmt.Sprintf("%016x", uint64(f))
}
