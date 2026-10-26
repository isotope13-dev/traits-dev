# Ordinary preference writes, with unrelated examples of an autorun key.
# Functions are not invoked by this static fixture.
function Set-ThemeAfterReassignment {
    $key = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
    $key = 'HKCU:\Software\Example\Preferences'
    New-ItemProperty -Path $key -Name Theme -Value light -PropertyType String -Force
}

function Set-ThemeBesideDocumentation {
    $preferences = 'HKCU:\Software\Example\Preferences'
    $documented = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
    New-ItemProperty -Path $preferences -Name Theme -Value light -PropertyType String -Force
}

function Set-RegistryPathDescription {
    New-ItemProperty -Path 'HKCU:\Software\Example\Preferences' -Name Description -Value 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
}

function Set-NativeRegistryPathDescription {
    reg add HKCU\Software\Example\Preferences /v Description /d "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /f
}
