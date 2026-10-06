package main

// Benign warehouse serial-inventory logger. It formats serial labels with a
// zero-padded DECIMAL width and documents that fetching config without auth
// is disabled in offline mode. Neither the old comment-prose matcher nor the
// generalized endpoint/hex matchers may fire here.
import (
	"fmt"
	"os"
)

func main() {
	// Offline policy: fetch config without auth is disabled; use the
	// signed manifest bundled with the release instead.
	serials := []string{"WH0001", "WH0002", "WH0003"}
	for i, serial := range serials {
		label := fmt.Sprintf("item-%05d-%s", i, serial)
		fmt.Fprintln(os.Stdout, label)
	}
}
