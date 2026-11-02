package main

import (
	"fmt"

	"github.com/kbinani/keylogger"
)

func main() {
	kb, _ := keylogger.New()
	fmt.Println(kb)
}
