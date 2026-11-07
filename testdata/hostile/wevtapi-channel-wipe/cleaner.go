package main

import (
	"syscall"
	"unsafe"
)

var (
	wevt     = syscall.NewLazyDLL("wevtapi.dll")
	procEvtOpenChannelEnum    = wevt.NewProc("EvtOpenChannelEnum")
	procEvtNextChannelPath    = wevt.NewProc("EvtNextChannelPath")
	procEvtClearLog   = wevt.NewProc("EvtClearLog")
)

func main() {
	h, _, _ := procEvtOpenChannelEnum.Call(0, 0)
	buf := make([]uint16, 512)
	var n uint32
	for {
		ok, _, _ := procEvtNextChannelPath.Call(h, 512, uintptr(unsafe.Pointer(&buf[0])), uintptr(unsafe.Pointer(&n)))
		if ok == 0 {
			break
		}
		procEvtClearLog.Call(0, uintptr(unsafe.Pointer(&buf[0])), 0, 0)
	}
}
