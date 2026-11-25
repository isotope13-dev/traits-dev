// +build windows
package main

import (
	"unsafe"

	"golang.org/x/sys/windows"
)

func main() {
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	CreateThread := kernel32.NewProc("CreateThread")
	addr, _, _ := VirtualAlloc.Call(0, 4096, 0x3000, 0x40)
	_ = unsafe.Pointer(addr)
	CreateThread.Call(0, 0, addr, 0, 0, 0)
}
