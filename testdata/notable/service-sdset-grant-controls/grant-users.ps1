# Allow interactive users to start and stop the print helper service.
sc.exe create PrintHelper binPath= "C:\Program Files\PrintHelper\helper.exe" start= demand
sc.exe sdset PrintHelper "D:(A;;CCLCSWRPWPDTLOCRRC;;;IU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)"
