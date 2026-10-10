$Native = @'
using System.Runtime.InteropServices;
public class CredApi {
    [DllImport("Advapi32.dll", EntryPoint = "CredEnumerateW")]
    public static extern bool Enumerate(string filter, int flags);
}
'@
Add-Type $Native
function CredManMain { Write-Output 'Credential metadata listing' }
