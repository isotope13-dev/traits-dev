local command = "Add-MpPreference -ExclusionPath $env:SystemDrive -ExclusionExtension .exe, .dll -Force"
print(command)
