package vector

// Benign control: a long hexadecimal test vector decoded for a checksum
// comparison. Carries payload-shaped data but stages and executes nothing,
// so it must never reach a hostile verdict.
import "encoding/hex"

var golden = "48656c6c6f2c20746869732069732061207465737420766563746f7220666f7220636865636b73756d20636f6d70617269736f6e20696e20776972652070726f746f636f6c2074657374732e"

func matches(input []byte) bool {
	raw, err := hex.DecodeString(golden)
	if err != nil {
		return false
	}
	if len(raw) != len(input) {
		return false
	}
	for i := range raw {
		if raw[i] != input[i] {
			return false
		}
	}
	return true
}
