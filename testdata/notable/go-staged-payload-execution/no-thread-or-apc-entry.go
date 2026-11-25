// +build windows
package main

import (
	"encoding/base64"
	"unsafe"

	"golang.org/x/sys/windows"
)

func main() {
	data, _ := base64.StdEncoding.DecodeString("U29tZUNvbmZpZ3VyYXRpb25CbG9iVGhhdElzTm90Q29kZVNvbWVDb25maWd1cmF0aW9uQmxvYg==")
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	addr, _, _ := VirtualAlloc.Call(0, uintptr(len(data)), 0x3000, 0x40)
	copy((*[1 << 20]byte)(unsafe.Pointer(addr))[:len(data)], data)
}
