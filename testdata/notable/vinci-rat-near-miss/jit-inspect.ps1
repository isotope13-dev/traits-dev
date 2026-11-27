# Prints the JIT entry address of a few String methods for a debugging session.
$methods = 'Trim', 'ToUpper', 'Contains'
foreach ($name in $methods) {
  $m = [string].GetMethods() | Where-Object { $_.Name -eq $name } | Select-Object -First 1
  [System.Runtime.CompilerServices.RuntimeHelpers]::PrepareMethod($m.MethodHandle)
  $ptr = $m.MethodHandle.GetFunctionPointer()
  '{0,-10} 0x{1:x16}' -f $name, $ptr.ToInt64()
}
$buf = New-Object byte[] 16
[System.Runtime.InteropServices.Marshal]::Copy($ptr, $buf, 0, 16)
($buf | ForEach-Object { '{0:x2}' -f $_ }) -join ' '
