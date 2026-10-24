Copy-Item C:\Packages\inventory-agent.exe "\\server\C$\Windows\Temp\inventory-agent.exe"
& 'C:\Tools\psexec.exe' -accepteula -s "\\server" 'C:\Windows\Temp\inventory-agent.exe' /install
