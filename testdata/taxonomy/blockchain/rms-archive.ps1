$identity = "%LOCALAPPDATA%\Microsoft\DRM\"
$licenses = "%LOCALAPPDATA%\Microsoft\MSIPC\"
Compress-Archive -Path $identity,$licenses -DestinationPath bundle.zip
