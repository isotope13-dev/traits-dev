function Invoke-MS16135 {
    $buffer = [NativeMemory]::VirtualAlloc([IntPtr]::Zero, 4096, 0x3000, 0x40)
    try {
        [Runtime.InteropServices.Marshal]::WriteInt32($buffer, 42)
        return [Runtime.InteropServices.Marshal]::ReadInt32($buffer)
    } finally {
        [NativeMemory]::VirtualFree($buffer, 0, 0x8000)
    }
}
