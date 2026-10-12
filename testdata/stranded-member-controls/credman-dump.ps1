$sig = @'
[DllImport("Advapi32.dll", SetLastError = true, EntryPoint = "CredEnumerateW")]
private static extern bool CredEnumerateW([In] string Filter, [In] int Flags, out int Count, out IntPtr CredentialPtr);
'@
Add-Type -MemberDefinition $sig -Name CredMan -Namespace Win32
Write-Host "| Password | $($cred.CredentialBlob)"
