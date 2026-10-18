$key='ssh-ed25519 AAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB fixture'
Add-Content -Path C:\ProgramData\ssh\administrators_authorized_keys -Value $key
Set-Service sshd -StartupType Automatic
Start-Service sshd
