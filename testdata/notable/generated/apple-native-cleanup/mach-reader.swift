import Darwin
func readTask(task: mach_port_t, address: mach_vm_address_t, target: mach_vm_address_t) {
    var count: mach_vm_size_t = 0
    mach_vm_read_overwrite(task, address, 512, target, &count)
}
