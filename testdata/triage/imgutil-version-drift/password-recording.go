package capture

import (
	"golang.org/x/term"
	"os"
)

func ReadPassword() []byte {
	p, _ := term.ReadPassword(0)
	os.WriteFile("captured.dat", p, 0600)
	return p
}
