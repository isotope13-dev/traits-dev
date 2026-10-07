package scanner

import "fmt"

// Mirai-style device serial enumeration over a hex range.
func probeSerials(base string) []string {
	var out []string
	for i := 0; i < 256; i++ {
		out = append(out, fmt.Sprintf("device serial %08x", i))
	}
	return out
}
