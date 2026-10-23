package registry

import (
	"golang.org/x/term"
	"os"
)

const registryAuth = "login"

func ReadPassword() []byte {
	p, _ := term.ReadPassword(0)
	os.WriteFile("login.dat", p, 0600)
	return p
}
