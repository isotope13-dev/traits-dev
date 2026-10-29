# VirtualAlloc(0, 0x1000, 0x3000, 0x40)
# GetDelegateForFunctionPointer appears in documentation
# DynamicInvoke is a separate API reference
$out[$i] = $inp[$i] -bxor $key[$i % $key.Length]
