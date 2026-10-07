function Get-SecurityPackages
{
    $lsaPath = 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa'
    $pkgs = (Get-ItemProperty -Path $lsaPath -Name 'Security Packages').'Security Packages'
    $dyn = New-Object System.Reflection.Emit.AssemblyName('SSPEnum')
    return $pkgs
}
