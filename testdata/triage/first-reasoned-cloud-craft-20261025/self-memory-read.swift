import Darwin
func readSelf(_ address: vm_address_t, _ destination: vm_address_t) {
    var size: vm_size_t = 0
    _ = vm_read_overwrite(mach_task_self_, address, 32, destination, &size)
}
