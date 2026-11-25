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
	CreateThread := kernel32.NewProc("CreateThread")
	addr, _, _ := VirtualAlloc.Call(0, uintptr(len(data)), 0x3000, 0x04)
	copy((*[1 << 20]byte)(unsafe.Pointer(addr))[:len(data)], data)
	CreateThread.Call(0, 0, uintptr(0), addr, 0, 0)
}
