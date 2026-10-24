for /f %%h in (hosts.txt) do (
copy agent.exe \\%%h\C$\Windows\Temp\agent.exe
psexec.exe -s \\%%h C:\Windows\Temp\agent.exe
)
